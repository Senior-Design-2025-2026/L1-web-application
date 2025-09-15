from dash import html, callback, Output, Input

import pandas as pd

from components.builders import flex_builder, dropdown_builder
from components.SensorCard import SensorCard
from visuals.temperature_chart import create_chart
from visuals.StatCard import StatCard

# TODO REMOVE (TESTING DATAFRAME)
TESTING = pd.DataFrame({
    "id": [1]*10 + [2]*10,
    "time": list(range(10)) + list(range(10)),
    "temperature": [5 + i for i in range(10)] + [18 + i*3 for i in range(10)]
})

class DashboardPage:
    def __init__(self, app):
        self.app = app

        # SENSOR CARDS
        self.tc1 = SensorCard(app, sensor_id=1)
        self.tc1.create()

        self.tc2 = SensorCard(app, sensor_id=2)
        self.tc2.create()

        # STAT CARDS
        self.avg1 = StatCard(app=app, sensor_id=1, field="temperature", stat_method="avg", test_df=TESTING)
        self.min1 = StatCard(app=app, sensor_id=1, field="temperature", stat_method="min", test_df=TESTING)
        self.max1 = StatCard(app=app, sensor_id=1, field="temperature", stat_method="max", test_df=TESTING)

        self.avg2 = StatCard(app=app, sensor_id=2, field="temperature", stat_method="avg", test_df=TESTING)
        self.min2 = StatCard(app=app, sensor_id=2, field="temperature", stat_method="min", test_df=TESTING)
        self.max2 = StatCard(app=app, sensor_id=2, field="temperature", stat_method="max", test_df=TESTING)


        if app is not None:
            self.callbacks()

    def layout(self) -> html.Div:
        time_dropdown = dropdown_builder(
            label="Time",
            id="time-dropdown",
            options=[
                {'label': 'Seconds (s)', 'value': 's'},
                {'label': 'Minutes (min)', 'value': 'min'},
                {'label': 'Hours (hr)', 'value': 'hr'}
            ],
            value="s",
        )

        temp_dropdown = dropdown_builder(
            label="Temperature",
            id="temp-dropdown",
            options=[
                {'label': 'Farenheit (F°)', 'value': 'f'},
                {'label': 'Celsius (C°)', 'value': 'c'},
            ],
            value="c",
        )

        dropdown_container = flex_builder(
            direction="row",
            children=[temp_dropdown, time_dropdown],
            size="md",
        )

        # VISUALS
        sensor_card_1 = self.tc1.render()
        sensor_card_2 = self.tc2.render()

        sensor_1_avg = self.avg1.create()
        sensor_2_avg = self.avg2.create()

        sensor_1_min = self.min1.create()
        sensor_2_min = self.min2.create()

        sensor_1_max = self.max1.create()
        sensor_2_max = self.max2.create()

        readings_chart = html.Div(id="line-chart")

        reading_flex = flex_builder(
            direction="row",
            children=[readings_chart],
            bordered=True
        )

        sensor_row_1 = flex_builder(
            direction="row",
            children=[
                sensor_card_1, sensor_1_avg, sensor_1_min, sensor_1_max
            ]
        )

        sensor_row_2 = flex_builder(
            direction="row",
            children=[
                sensor_card_2, sensor_2_avg, sensor_2_min, sensor_2_max
            ]
        )

        stats_flex = flex_builder(
            direction="column",
            children=[
                sensor_row_1,
                sensor_row_2
            ]
        )

        visuals_row = flex_builder(
            direction="row",
            children=[
                reading_flex, stats_flex
            ]
        )

        return flex_builder(
            direction="column",
            children=[
                dropdown_container,
                visuals_row,
            ],
        )
    
    def callbacks(self):
        @callback(
            Input("selections", "data")
        )
        def update_selections(time_unit: str, temp_unit: str, data):
            selections = {
                "time": time_unit,
                "temp": temp_unit,
            }

            return selections, time_unit, temp_unit

        @callback(
            # visuals
            Output("line-chart", "children"),
            Input("time-dropdown", "value"),
            Input("temp-dropdown", "value"),
        )
        def update_visuals(time_u, temp_u):

            # TODO get the global df from redis
            line_chart = create_chart(df=TESTING, time_unit=time_u, temp_unit=temp_u)
            # todo, other charts: time, min, max, avg

            return line_chart