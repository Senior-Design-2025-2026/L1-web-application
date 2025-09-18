from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from flask import Flask
from flask import request

from pages.dashboard import DashboardPage
from pages.settings import SettingsPage
from components.footer import footer

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# from db_conn.db_methods import DBConnection

server = Flask(__name__)

app = Dash(__name__, 
        server=server, 
        suppress_callback_exceptions=True, 
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        prevent_initial_callbacks="initial_duplicate",
        assets_folder="./assets"
        )

# ------------------- NAVBAR ------------------ #
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard")),
        dbc.NavItem(dbc.NavLink("Settings", href="/settings"))
    ],
    brand="Lab 1",
    brand_href="/",
    color="primary",
    dark=True
)


# ------------------- FOOTER ------------------ #
linkedIn_links = {
    "Matt Krueger": "https://www.linkedin.com/in/mattnkrueger/",
    "Sage Marks": "https://www.linkedin.com/in/sage-marks/",
    "Steven Austin": "https://wwww.linkedin.com/in/steven-austin-does-not-have-a-linked-in",
    "Zack Mulholland": "https://www.linkedin.com/in/zack-mulholland-317914254/",
}

project_links = {
    "Github": "https://github.com/Senior-Design-2025-2026",
    "Server Code": "https://github.com/Senior-Design-2025-2026/L1-web-server",
    "Embedded Code": "https://github.com/Senior-Design-2025-2026/L1-embedded-thermostat"
}

footer = footer(project_links=project_links, linkedIn_links=linkedIn_links)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content'),
    footer
])


# ---------------- DB CONNECTION ---------------- #
db_path = "app/db_conn/Lab1.db"
# db_conn = DBConnection(db_path=db_path)

# ------------------ APP PAGES ------------------ #   
dashboard_page_obj = DashboardPage(app)
settings_page_obj  = SettingsPage(app)

# ----------------- APP ROUTING ----------------- #   
@server.route('/temperatureData', methods = ['POST'])
def getTemperatureData():

    tempData = request.get_json()

    # Shift temperature columns up to remove oldest data (first row)
    dashboard_page_obj.df["temperatureSensor1Data"] = dashboard_page_obj.df["temperatureSensor1Data"].shift(-1)
    dashboard_page_obj.df["temperatureSensor2Data"] = dashboard_page_obj.df["temperatureSensor2Data"].shift(-1)
    
    # Append new temperature data to the last row
    dashboard_page_obj.df.iloc[-1, dashboard_page_obj.df.columns.get_loc("temperatureSensor1Data")] = int(tempData["sensor1Temperature"])
    dashboard_page_obj.df.iloc[-1, dashboard_page_obj.df.columns.get_loc("temperatureSensor2Data")] = int(tempData["sensor2Temperature"])

    if (int(tempData["sensor1Temperature"]) > dashboard_page_obj.threshold):
        if not dashboard_page_obj.overThreshold:
            dashboard_page_obj.overThreshold = True
        else:
            me = "insertyouremail@uiowa.edu"
            you = "insertyouremail@uiowa.edu"

            msg = MIMEText("Temperature read over 40 degrees C")
            msg["Subject"] = "Temperature Over Threshold"
            msg["From"] = me
            msg["To"] = you

            with smtplib.SMTP("ns-mx.uiowa.edu", 25) as server:
                server.sendmail(me, [you], msg.as_string())
    else:
        dashboard_page_obj.overThreshold = False

    return "Success", 200


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/' or pathname == '/dashboard':
        return dashboard_page_obj.layout()
    elif pathname == '/settings':
        return settings_page_obj.layout()
    else:
        return html.Div("404 Page Not Found")

if __name__ == '__main__':
    app.run(debug=True, port=8050)