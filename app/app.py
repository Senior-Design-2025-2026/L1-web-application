import dash
from dash import Dash, html, dcc, Input, Output, clientside_callback, _dash_renderer, State
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import redis
import os

import time

from pathlib import Path

from pages.live import LivePage
from pages.analytics import AnalyticsPage
from pages.settings import SettingsPage

from components.shell.header import header
from components.shell.footer import footer

from database.db_methods import DB

# ===================================================
#                  REDIS STREAM
# ===================================================
# we are using redis stream to communicate between the 
# c/c++ embedded code and the web server.
redis = redis.Redis(
        host="redis",
        port=6379,
        decode_responses=True
)

# ===================================================
#                 SYSTEM CLOCK 
# ===================================================
# configures app to refresh every INTERVAL seconds
# docs: https://dash.plotly.com/dash-core-components/interval
INTERVAL = 1

# ===================================================
#                 DATABASE OBJECT
# ===================================================
# using sqlalchemy to handle crudding
# (see db_orm and db_methods for implementation details)
# docs: https://www.sqlalchemy.org/
db_path = "app/database/sqlite/lab1.db"
DB = DB(db_path=db_path)

# ===================================================
#                 DASH APPLICATION
# ===================================================
# This is a python Plotly Dash application
# plotly dash: https://dash.plotly.com/
# mantine components: https://www.dash-mantine-components.com/

app = Dash(
    name="ECE Senior Design Lab 1", 
    assets_folder=str(Path.cwd() / "app" / "assets"),
    suppress_callback_exceptions=True
)

app.title = "Lab 1: ECE Senior Design"

live_page_obj      = LivePage(db=DB, app=app)
analytics_page_obj = AnalyticsPage(db=DB, app=app)
settings_page_obj  = SettingsPage(db=DB, app=app)

app.layout = dmc.MantineProvider(
    theme={
        "primaryColor": "yellow",
        "defaultRadius": "sm",
        "black": "#454545",  
        "components": {
            "Button": {
                "defaultProps": {
                    "shadow": "xs"
                }
            },
            "Card": {
                "defaultProps": {
                    "shadow": "xs",
                    "radius": "sm"
                }
            },
        },
    },
    children=[
        dcc.Store(id="cache"),
        dcc.Location(id='url'),
        dcc.Interval(
            id="system-clock",
            interval=(INTERVAL * 1000),                 # in ms! 
            n_intervals=0

        ),
        dmc.AppShell(
            [
                dmc.AppShellHeader(
                    header()
                ),
                dmc.AppShellMain(
                    dmc.Box(
                        id="page-content",
                        py="sm",
                        px="sm",
                    ),
                ),
                footer()
            ],
            header={"height":60, "width":"100%"},
        )
    ],
)


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/' or pathname == '/live':
        return live_page_obj.layout()
    elif pathname == '/analytics':
        return analytics_page_obj.layout()
    elif pathname == '/settings':
        return settings_page_obj.layout()
    else:
        return html.Div("404 Page Not Found")

PORT = os.getenv("DASH_PORT", "8050")
HOST = os.getenv("HOST", "0.0.0.0")

if __name__ == '__main__':


    app.run(
        debug=True,
        port=PORT,
        host=HOST            
    )
