from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc

from components.builders import flex_builder, dropdown_builder
from components.SensorCard import SensorCard
from visuals.temperature_chart import create_chart

class DashboardPage:
    def __init__(self, app):
        self.app = app

        self.tc1 = SensorCard(app, sensor_id=1)
        self.tc1.create()

        self.tc2 = SensorCard(app, sensor_id=2)
        self.tc2.create()

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

        temp_card_1 = self.tc1.render()
        temp_card_2 = self.tc2.render()

        temp_cards = html.Div(
            flex_builder(
                direction="row",
                children=[
                    temp_card_1,
                    temp_card_2
                ],
                alignment="center",
                justification="center",
            ),
            style={
                "width":"100%",
                "height":"100%",
            }
        )

        readings_chart = html.Div(id="line-chart")

        return flex_builder(
            direction="column",
            children=[
                dropdown_container,
                readings_chart,
                temp_cards
            ],
        )
    
    def callbacks(self):
        @callback(
            Output("selections", "data"),
            Input("time-dropdown", "value"),
            Input("temp-dropdown", "value"),
        )
        def update_selections(time_val: str, temp_val: str):
            return {
                "time": time_val,
                "temp": temp_val,
            }

        @callback(
            # visuals
            Output("line-chart", "children"),
            Input("selections", "data")
        )
        def update_visuals(selections):
            time_unit = selections.get("time")
            temp_unit = selections.get("temp")

            # TODO get the global df from redis
            line_chart = create_chart(df=None, time_unit=time_unit, temp_unit=temp_unit)
            # todo, other charts: time, min, max, avg

            return line_chart