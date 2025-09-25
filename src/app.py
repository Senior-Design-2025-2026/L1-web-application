from dash import Dash, html, dcc, Input, Output, ctx
import dash_mantine_components as dmc
import redis
import os
from components.aio.thermostat_card import ThermostatCardAIO

from pathlib import Path

from pages.live import LivePage
from pages.analytics import AnalyticsPage
from pages.settings import SettingsPage

from components.shell.header import header
from components.shell.footer import footer
from celery import Celery

from db.db_methods import DB

# ===================================================
#                ENVIRONMENT VARIABLES
# ===================================================
HOST    = os.getenv("HOST", "0.0.0.0")      # default for if using uv in dev
PORT    = os.getenv("PORT", "8050")         # ^^^
SOCK    = os.getenv("SOCK")
DB_URL = os.getenv("DB_URL")

if not HOST:
    raise RuntimeError("HOST env var is not set")
if not PORT:
    raise RuntimeError("PORT env var is not set")
if not SOCK:
    raise RuntimeError("SOCK env var is not set")
if not DB_URL:
    raise RuntimeError("DB_PATH env var is not set")

# ===================================================
#                REDIS STREAM + CACHE
# ===================================================
red = redis.Redis(
    unix_socket_path=SOCK,
    decode_responses=True
)

# ===================================================
#                CELERY TASK QUEUE
# ===================================================
celery_client = Celery(
    main=__name__,
    broker=f"redis+socket://{SOCK}",
)

# ===================================================
#                 SYSTEM CLOCK 
# ===================================================
INTERVAL = 1

# ===================================================
#                 DATABASE OBJECT
# ===================================================
DB = DB(db_path=DB_URL)

# ===================================================
#                 DASH APPLICATION
# ===================================================
app = Dash(
    name="ECE Senior Design Lab 1", 
    assets_folder=str(Path.cwd() / "src" / "assets"),
    suppress_callback_exceptions=True
)

app.title = "Lab 1: ECE Senior Design"

live_page_obj      = LivePage(app=app, redis=red)
analytics_page_obj = AnalyticsPage(app=app, db=DB)
settings_page_obj  = SettingsPage(app=app, db=DB, celery=celery_client)

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

# ===================================================
#                FLASK HTTP ROUTING
# ===================================================
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

if __name__ == '__main__':
    app.run(
        debug=True,
        port=PORT,
        host=HOST            
    )
