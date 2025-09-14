from dash import html, dcc, callback, Output, Input

from components.dropdown_builder import dropdown_builder
from components.flex_builder import flex_builder
from components.TemperatureCard import TemperatureCard

class DashboardPage:
    def __init__(self, app):
        self.app = app
        self.tc1 = TemperatureCard(app, sensor_id=1)
        self.tc2 = TemperatureCard(app, sensor_id=2)

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
            reversed=False
        )

        temp_card_1 = html.Div(
            id="temp-card-1"
        )

        temp_card_2 = html.Div(
            id="temp-card-2"
        )

        temp_cards = flex_builder(
            direction="row",
            children=[
                temp_card_1,
                temp_card_2
            ]
        )

        return html.Div([
            dropdown_container, temp_cards
        ])
    
    def callbacks(self):
        @callback(
            Output("temp-card-1", "children"),
            Input("time-dropdown", "value"),
        )
        def time_selection(time):
            self.tc1.turn_off()
            return self.tc1.render()

        @callback(
            Output("temp-card-2", "children"),
            Input("temp-dropdown", "value"),
        )
        def temp_selection(temp):
            self.tc2.turn_on()
            self.tc2.update({"temp": "20"})
            return self.tc2.render()