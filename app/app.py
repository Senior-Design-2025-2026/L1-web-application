from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from flask import Flask

from pages.dashboard import DashboardPage
from pages.settings import SettingsPage

server = Flask(__name__)

app = Dash(__name__, 
        server=server, 
        suppress_callback_exceptions=True, 
        external_stylesheets=[dbc.themes.BOOTSTRAP]
        )

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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

# ----------------- APP ROUTING ----------------- #   
dashboard_page_obj = DashboardPage(app)
settings_page_obj  = SettingsPage(app)

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
    app.run(debug=True)