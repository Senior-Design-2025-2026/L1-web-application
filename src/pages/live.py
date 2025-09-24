from dash import Input, Output, callback
import dash_mantine_components as dmc
import pandas as pd
from io import StringIO
from utils.temperature_utils import c_to_f, c_to_k

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

        # literally spend an 1 hr debugging "Error: Objects are not valid as a React child"
        #               card_1 = ThermostatCardAIO("Sensor 1", aio_id="1"),
        #                                                                ~~~
        # DO NOT HAVE TRAILING "," this creates a tuple like so (ThemostatCardAIO, )
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
                {"value": "k", "label": "Kelvin (K)"},
                {"value": "f", "label": "Fahrenheit (°F)"},
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
                    ]
                )
            ],
        )

        return home

    def callbacks(self):
        @callback(
            Output("readings-chart", "data"),
            Output("readings-chart", "unit"),
            Input("system-clock", "n_intervals"),
            Input("unit-dropdown", "value"),
        )
        def update_chart(n_intervals, unit):
            try:
                b_data = self.red.get("current_df")
                df = pd.read_json(StringIO(b_data))

                temperature_cols = ["Sensor 1", "Sensor 2"]
                if unit == "f":
                    df[temperature_cols] = df[temperature_cols].apply(c_to_f)
                elif unit == "k":
                    df[temperature_cols] = df[temperature_cols].apply(c_to_k)
                records = df.to_dict("records")
            except:
                records = pd.DataFrame()

            return records, f"°{unit.upper()}"
