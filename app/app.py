from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from flask import Flask
import plotly.express as px

from pages.dashboard import DashboardPage
from pages.settings import SettingsPage

################### DATA SHARING AND STORAGE ####################
# Dash is session based per client which makes viewing and 
# modifying the system between multiple uses troublesome

# We want the status and stream of data to be identical across 
# clients. For example, if client 'a' turns sensor 1 on, then 
# this is reflected within client 'b's view

# For performance and persistence, we employ the following items

# 1. GLOBAL: Redis 
# --- what is stored globally?
# - sensor 1 status
# - sensor 2 status
# - streaming data 

# 2. SESSION: dcc.Store (client side browser cache)
# --- what is being cached locally?
# - temperature selection
# - timeframe selection

# 3. DATABASE: Sqlite
# --- what data is persisting?
# - streaming data (write through by the embedded program...)
################################################################

server = Flask(__name__)

app = Dash(__name__, 
        server=server, 
        suppress_callback_exceptions=True, 
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        prevent_initial_callbacks="initial_duplicate"
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
    dcc.Store(id="store"),                                              # using to store client session selections; NOT using to store df as this is streamed
    
    # actual html part
    navbar,
    html.Div(id='page-content'),
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
    app.run(debug=True, host='0.0.0.0', port=8050)