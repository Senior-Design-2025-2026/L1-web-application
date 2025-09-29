RANGE_C = [0, 10, 20, 30, 40, 50]           # hardcoded... this is verified. didnt want to include functions for these
RANGE_F = [32, 50, 68, 86, 104, 122]        # maybe a different scale so there isnt an illusion that c -> f didnt spike temp.
RANGE_K = [273, 283, 293, 303, 313, 323]    # looks a little odd due to the formula
from dash import Input, Output, callback, ctx, html, State
from numpy import nan_to_num
import dash_mantine_components as dmc
import pandas as pd
from io import StringIO
from utils.temperature_utils import c_to_f, c_to_k
from utils.process_stream import process_stream

from components.aio.thermostat_card import ThermostatCardAIO, RANGE_C, RANGE_F, RANGE_K

pd.set_option("display.max_rows", 20)
pd.set_option("display.max_columns", 20)

SENSOR_1_COLOR = "#e85d04"
SENSOR_2_COLOR = "#ffba08"

def nan_to_none(temp):
    return None if pd.isna(temp) else temp

class LivePage:
    def __init__(self, app, redis):
        self.red = redis
        
        if app is not None:
            self.callbacks()

    def layout(self):
        self.red.set("button_1_status", "ON")
        card_1 = ThermostatCardAIO("Sensor 1", aio_id="1", color=SENSOR_1_COLOR)
        card_2 = ThermostatCardAIO("Sensor 2", aio_id="2", color=SENSOR_2_COLOR)

        cards = dmc.Stack(
            [
                card_1,
                card_2
            ],
            justify="center",
            align="center"
        )

        line_chart = dmc.Card(
            dmc.LineChart(
                id="readings-chart",
                h=550,
                w=900,
                data=[],
                series=[
                    {"name": "Sensor 1", "color": SENSOR_1_COLOR},
                    {"name": "Sensor 2", "color": SENSOR_2_COLOR},
                ],
                dataKey="date",
                curveType="Linear",

                tickLine="y",
                gridAxis="x",
                withXAxis="True",
                xAxisLabel="Time (s)",

                withYAxis="True",
                yAxisLabel="Temperature",

                withDots="True",
                withLegend=True,
                connectNulls=False,
            ),
            withBorder=True,
        )

        segment = dmc.Select(
            id="unit-dropdown-live",
            data=[
                {"value": "c", "label": "Celcius (°C)"},
                {"value": "f", "label": "Fahrenheit (°F)"},
                {"value": "k", "label": "Kelvin (K)"},
            ],
            value="c",
            size="md",
            persistence=True
        )

        clear = dmc.Button(
            id="clear-stream",
            children="Clear",
            size="md"
        )

        home = dmc.Group(
            [
                cards,
                dmc.Stack(
                    [
                        dmc.Grid(
                            children = [
                                dmc.GridCol(dmc.Box(segment), span=10),
                                dmc.GridCol(dmc.Box(clear), span=2),
                            ],
                            grow=True,
                            gutter="md"
                        ),

                        line_chart,
                        html.Div(id="empty")
                    ]
                )
            ],
        )

        return home
    
    def get_segment_color(self, status:str):
        return "green" if status == "ON" else "red"

    def callbacks(self):
        @callback(
            Output("readings-chart", "data"),
            Output("readings-chart", "unit"),
            Output("readings-chart", "yAxisProps"),
            Output(ThermostatCardAIO.ids.data("1"), "data"),
            Output(ThermostatCardAIO.ids.data("2"), "data"),
            Input("system-clock", "n_intervals"),
            Input("unit-dropdown-live", "value"),
        )
        def update_chart(n_intervals, unit):
            data = self.red.xrevrange(name="readings", count=300)

            df = (process_stream(data))

            if df is not None:
                df = df.where(pd.notna(df), None)
                try:
                    first_row = df.iloc[[-1]]
                    sensor_1_temp = nan_to_none(first_row.iloc[0]["Sensor 1"])
                    sensor_2_temp = nan_to_none(first_row.iloc[0]["Sensor 2"])
                except:
                    sensor_1_temp = None
                    sensor_2_temp = None

                temperature_cols = ["Sensor 1", "Sensor 2"]
                if unit == "f":
                    df[temperature_cols] = df[temperature_cols].apply(c_to_f)
                    range_y = [RANGE_F[0], RANGE_F[-1]]
                elif unit == "k":
                    df[temperature_cols] = df[temperature_cols].apply(c_to_k)
                    range_y = [RANGE_K[0], RANGE_K[-1]]
                else:
                    range_y = [RANGE_C[0], RANGE_C[-1]]
                
                df["date"] = pd.to_datetime(df["date"], unit="s")
                df["date"] = df["date"].dt.tz_localize("UTC")
                df["date"] = df["date"].dt.tz_convert("America/Chicago")
                df["date"] = df["date"].dt.time
            else:
                first_row = "NO DATA"
                sensor_1_temp = None
                sensor_2_temp = None
                range_y = [RANGE_C[0], RANGE_C[-1]]

            records = df.to_dict("records")

            # CLIENT-SIDE CACHE TEMPERATURE READINGS
            # hacky, but works - was having troubles adding an instance of the redis stream into the AIO component.
            # using client-side cache to trigger the updates. Works out nicely as the completion of this callback
            # will ultimately trigger the AIO callbacks simulatneously. 
            thermostat_card_1 = {"val": str(sensor_1_temp)}
            thermostat_card_2 = {"val": str(sensor_2_temp)}

            # range of chart
            yAxisProps = {"domain":range_y}

            return records, f"°{unit.upper()}", yAxisProps, thermostat_card_1, thermostat_card_2

        @callback(
            Output("empty", "children"),
            Input("clear-stream", "n_clicks")
        )
        def clear_stream(n_clicks):
            if ctx.triggered_id == "clear-stream":          
                self.red.delete("readings")
            return [""]

        # ==========================================
        #            HANDLE SENSOR TOGGLES
        # ==========================================
        @callback(
            Output(ThermostatCardAIO.ids.segmented_control("1"), "value"),
            Output(ThermostatCardAIO.ids.segmented_control("1"), "color"),
            Input("system-clock", "n_intervals"),
            Input(ThermostatCardAIO.ids.segmented_control("1"), "value")
        )
        def toggle_sensor_1(n_intervals, wanted):
            actual = self.red.get("virtual:1:status")

            if ctx.triggered_id == ThermostatCardAIO.ids.segmented_control("1"):
                if wanted != actual:              
                    self.red.set("virtual:1:wants_toggle", "true")
            
            segment_color = self.get_segment_color(actual)

            return actual, segment_color

        @callback(
            Output(ThermostatCardAIO.ids.segmented_control("2"), "value"),
            Output(ThermostatCardAIO.ids.segmented_control("2"), "color"),
            Input("system-clock", "n_intervals"),
            Input(ThermostatCardAIO.ids.segmented_control("2"), "value")
        )
        def toggle_sensor_2(n_intervals, wanted):
            actual = self.red.get("virtual:2:status")

            if ctx.triggered_id == ThermostatCardAIO.ids.segmented_control("2"):
                if wanted != actual:              
                    self.red.set("virtual:2:wants_toggle", "true")

            segment_color = self.get_segment_color(actual)

            return actual, segment_color
