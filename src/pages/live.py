from dash import Input, Output, callback, ctx, html
import dash_mantine_components as dmc
import pandas as pd
from io import StringIO
from utils.temperature_utils import c_to_f, c_to_k
from utils.process_stream import process_stream

from components.aio.thermostat_card import ThermostatCardAIO

SENSOR_1_COLOR = "#e85d04"
SENSOR_2_COLOR = "#ffba08"

class LivePage:
    def __init__(self, app, redis=None):
        self.red = redis
        
        if app is not None:
            self.callbacks()

    def layout(self):
        dropdown = dmc.Select(
            label="Select your favorite library",
            placeholder="Select one",
            id="framework-select",
            value="pd",
            data=[
                {"value": "pd", "label": "Pandas"},
                {"value": "np", "label": "NumPy"},
                {"value": "tf", "label": "TensorFlow"},
                {"value": "torch", "label": "PyTorch"},
            ],
            w=200,
            mb=10,
        )        

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
            ),
            withBorder=True,
        )

        segment = dmc.Select(
            id="unit-dropdown",
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

    def callbacks(self):
        @callback(
            Output("readings-chart", "data"),
            Output("readings-chart", "unit"),
            Output(ThermostatCardAIO.ids.data("1"), "data"),
            Output(ThermostatCardAIO.ids.data("2"), "data"),
            Input("system-clock", "n_intervals"),
            Input("unit-dropdown", "value"),
        )
        def update_chart(n_intervals, unit):
            try:
                data = self.red.xrevrange(name="readings", count=300)
                df = (process_stream(data))
            except:
                df = pd.DataFrame(columns=["date", "Sensor 1", "Sensor 2"])    

            try:
                first_row = df.iloc[[-1]]
                sensor_1_temp = first_row.iloc[0]["Sensor 1"]
                sensor_2_temp = first_row.iloc[0]["Sensor 2"]
            except:
                first_row = "NO DATA"
                sensor_1_temp = "missing"
                sensor_2_temp = "missing"

            temperature_cols = ["Sensor 1", "Sensor 2"]
            if unit == "f":
                df[temperature_cols] = df[temperature_cols].apply(c_to_f)
            elif unit == "k":
                df[temperature_cols] = df[temperature_cols].apply(c_to_k)
            records = df.to_dict("records")

            # CLIENT-SIDE CACHE TEMPERATURE READINGS
            # hacky, but works - was having troubles adding an instance of the redis stream into the AIO component.
            # using client-side cache to trigger the updates. Works out nicely as the completion of this callback
            # will ultimately trigger the AIO callbacks simulatneously. 
            thermostat_card_1 = {"val": str(sensor_1_temp)}
            thermostat_card_2 = {"val": str(sensor_2_temp)}
            return records, f"°{unit.upper()}", thermostat_card_1, thermostat_card_2

        @callback(
            Output("empty", "children"),
            Input("clear-stream", "n_clicks")
        )
        def clear_stream(n_clicks):
            if ctx.triggered_id == "clear-stream":          
                self.red.delete("readings")
            return [""]