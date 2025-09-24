from dash import Dash, html, dcc, Input, Output, ctx
import dash_mantine_components as dmc
import redis
import os
from components.aio.thermostat_card import ThermostatCardAIO

from utils.process_stream import process_stream


from pathlib import Path

from pages.live import LivePage
from pages.analytics import AnalyticsPage
from pages.settings import SettingsPage

from components.shell.header import header
from components.shell.footer import footer

from database.db_methods import DB, add_reading

# environment variables (see lab1/.env)
HOST    = os.getenv("HOST", "0.0.0.0")
PORT    = os.getenv("PORT", "8050")
SOCK    = os.getenv("SOCK")
DB_PATH = os.getenv("DB_PATH", "app/database/sqlite/lab1.db")

# ===================================================
#                REDIS STREAM + CACHE
# ===================================================
# we are using redis stream to communicate between the 
# additionally, we are using the redis cache to hold
# the processed dataframe to limit computation within 
# callbacks. 
red = redis.Redis(
    unix_socket_path=SOCK,
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
DB = DB(db_path=DB_PATH)

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

live_page_obj      = LivePage(app=app, redis=red)
analytics_page_obj = AnalyticsPage(app=app, db=DB)
settings_page_obj  = SettingsPage(app=app, db=DB)

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

@app.callback(
    Output(ThermostatCardAIO.ids.data("1"), "data"),
    Output(ThermostatCardAIO.ids.data("2"), "data"),
    Input("system-clock", "n_intervals"),
    Input("clear-stream", "n_clicks")
)
def process_and_cache(n_intervals, n_clicks):
    inv = -99
    if ctx.triggered_id == "clear-stream":          
        print("CLEARING STREAM")
        red.delete("readings")
        t1 = inv
        t2 = inv
    else:                      
        try:
            data = red.xrevrange(name="readings", count=300)
            df = (process_stream(data))
            red.set("current_df", df.to_json())
            first_row = df.iloc[[-1]]

            stamp = int(first_row.iloc[0]["date"])
            t1 = first_row.iloc[0]["Sensor 1"]
            t2 = first_row.iloc[0]["Sensor 2"]

            # write to database in the background       TODO
            # add_reading.delay(sensor_id=1, timestamp=stamp, temperature=t1)
            # add_reading.delay(sensor_id=2, timestamp=stamp, temperature=t2)

        except Exception as e:
            print("EXCEPTION: ", e)
            t1 = inv
            t2 = inv

    dat1 = {"val": str(t1)}
    dat2 = {"val": str(t2)}
    return dat1, dat2

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