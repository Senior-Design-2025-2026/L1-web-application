from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from flask import Flask, request, jsonify

from pages.dashboard import DashboardPage
from pages.settings import SettingsPage
from components.footer import footer

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Conversion functions
def celsiusToFahrenheit(temperature):
    if float(temperature) > 50:
        temperature = "50"
    elif float(temperature) < 10:
        temperature = "10"
    return float(temperature) * 9/5 + 32

sensor1Toggled = False
lastSensor1Value = True
sensor2Toggled = False
lastSensor2Value = True


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

    global lastSensor1Value, lastSensor2Value
    global sensor1Toggled, sensor2Toggled

    tempData = request.get_json()

    temperature1 = 0
    temperature2 = 0

    if tempData["sensor1Temperature"] == None:
        temperature1 = None
    elif dashboard_page_obj.unit == 'F':
        temperature1 = celsiusToFahrenheit(tempData["sensor1Temperature"])
    else:
        temperature1 = float(tempData["sensor1Temperature"])
        if temperature1 > 50:
            temperature1 = 50
        elif temperature1 < 10:
            temperature1 = 10

    if tempData["sensor2Temperature"] == None:
        temperature2 = None
    elif dashboard_page_obj.unit == 'F':
        temperature2 = celsiusToFahrenheit(tempData["sensor2Temperature"])
    else:
        temperature2 = float(tempData["sensor2Temperature"])
        if temperature2 > 50:
            temperature2 = 50
        elif temperature2 < 10:
            temperature2 = 10

    # Update labels in dashboard
    if temperature1 == None:
        dashboard_page_obj.set_temp1_label("Sensor1: Error")
    else:
        dashboard_page_obj.set_temp1_label("Sensor 1: " + str(int(temperature1)) + " " + dashboard_page_obj.unit)

    # Update labels in dashboard
    if temperature2 == None:
        dashboard_page_obj.set_temp2_label("Sensor2: Error")
    else:
        dashboard_page_obj.set_temp2_label("Sensor 2: " + str(int(temperature2)) + " " + dashboard_page_obj.unit)


    # Shift temperature columns up to remove oldest data (first row)
    dashboard_page_obj.df["temperatureSensor1Data"] = dashboard_page_obj.df["temperatureSensor1Data"].shift(1)
    dashboard_page_obj.df["temperatureSensor2Data"] = dashboard_page_obj.df["temperatureSensor2Data"].shift(1)
    

    # Append new temperature data to the last row
    dashboard_page_obj.df.iloc[0, dashboard_page_obj.df.columns.get_loc("temperatureSensor1Data")] = temperature1
    dashboard_page_obj.df.iloc[0, dashboard_page_obj.df.columns.get_loc("temperatureSensor2Data")] = temperature2

    if (settings_page_obj.saved_email is not None and (temperature1 != None and temperature1 > settings_page_obj.max_temperature or 
        temperature2 != None and temperature2 > settings_page_obj.max_temperature)):
        if not dashboard_page_obj.overThreshold:
            me = "seniordesignteam3@uiowa.edu"
            you = settings_page_obj.saved_email

            msg = MIMEText(f"Temperature read over {settings_page_obj.max_temperature} degrees C")
            msg["Subject"] = "Temperature Over Threshold"
            msg["From"] = me
            msg["To"] = you

            with smtplib.SMTP("ns-mx.uiowa.edu", 25) as server:
                server.sendmail(me, [you], msg.as_string())

            # Only send once
            dashboard_page_obj.overThreshold = True
    else:
        dashboard_page_obj.overThreshold = False

    if (settings_page_obj.saved_email is not None and (temperature1 != None and temperature1 < settings_page_obj.min_temperature or 
        temperature2 != None and temperature2 < settings_page_obj.min_temperature)):
        if not dashboard_page_obj.underThreshold:
            me = "seniordesignteam3@uiowa.edu"
            you = settings_page_obj.saved_email

            msg = MIMEText(f"Temperature read under {settings_page_obj.min_temperature} degrees C")
            msg["Subject"] = "Temperature Over Threshold"
            msg["From"] = me
            msg["To"] = you

            with smtplib.SMTP("ns-mx.uiowa.edu", 25) as server:
                server.sendmail(me, [you], msg.as_string())

            # Only send once
            dashboard_page_obj.underThreshold = True
    else:
        dashboard_page_obj.underThreshold = False

    
    # Handling a potential user toggle
    if dashboard_page_obj.tc1._active != lastSensor1Value:
        sensor1Toggled = True
        lastSensor1Value = dashboard_page_obj.tc1._active
    else:
        sensor1Toggled = False

    # Handling a potential user toggle
    if dashboard_page_obj.tc2._active != lastSensor2Value:
        sensor2Toggled = True
        lastSensor2Value = dashboard_page_obj.tc2._active
    else:
        sensor2Toggled = False

    return jsonify([
                dashboard_page_obj.unit,
                sensor1Toggled,
                sensor2Toggled
            ]), 200


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
    app.run(debug=True, port=8050, host="0.0.0.0")
