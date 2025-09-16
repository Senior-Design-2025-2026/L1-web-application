from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from flask import Flask

from pages.dashboard import DashboardPage
from pages.settings import SettingsPage

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
    brand="ECE Senior Design Lab 1: Temperature System",
    brand_href="/",
    color="secondary",
    dark=True
)


# ------------------- Footer Links ------------------ #
linkedIn_links = {
    "Matt Krueger": "https://www.linkedin.com/in/mattnkrueger/",
    "Sage Marks": "https://www.linkedin.com/in/sage-marks/",
    "Steven Austin": "https://wwww.linkedin.com/in/steven-austin-does-not-have-a-linked-in",
    "Zack Mulholland": "https://www.linkedin.com/in/zack-mulholland-317914254/",
}

project_links = {
    "Project Requirements": "https://github.com/Senior-Design-2025-2026/L1-web-server/blob/main/lab-1.pdf",
    "Team Github": "https://github.com/Senior-Design-2025-2026",
    "Server Code": "https://github.com/Senior-Design-2025-2026/L1-web-server",
    "Embedded Code": "https://github.com/Senior-Design-2025-2026/L1-embedded-thermostat",
}


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content'),
])

# ---------------- DB CONNECTION ---------------- #
db_path = "app/db_conn/Lab1.db"
# db_conn = DBConnection(db_path=db_path)

# ------------------ APP PAGES ------------------ #   
dashboard_page_obj = DashboardPage(app)
settings_page_obj  = SettingsPage(app)

# ----------------- APP ROUTING ----------------- #   
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
    app.run(debug=True, port="8050")
