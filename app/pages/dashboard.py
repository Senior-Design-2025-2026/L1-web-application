from dash import html, callback, Output, Input, dcc

import pandas as pd

from components.builders import flex_builder, dropdown_builder
from components.SensorCard import SensorCard
from visuals.temperature_chart import create_chart
from visuals.StatCard import StatCard

# Conversion functions
def celsiusToFahrenheit(temperature):
    if temperature is None:
        return None
    return temperature * 9/5 + 32

def fahrenheitToCelsius(temperature):
    if temperature is None:
        return None
    return (temperature - 32) * 5/9


class DashboardPage:
    def __init__(self, app):
        self.app = app

        self.df = pd.DataFrame({
            "id": [1]*301,
            "time": list(range(301)),
            "temperatureSensor1Data": [None for _ in range(301)],
            "temperatureSensor2Data": [None for _ in range(301)]
        })

        # SENSOR CARDS
        self.tc1 = SensorCard(app, sensor_id=1)
        self.tc1.create()

        self.tc2 = SensorCard(app, sensor_id=2)
        self.tc2.create()

        # Labels for the temperatures
        self.sensor1Temperature = "Temperature 1: "
        self.sensor2Temperature = "Temperature 2: "

        self.overThreshold = False
        self.underThreshold = False

        # Fields so the app can see the status and communicate with the sensor program
        self.unit = "C"
        self.sensor1On = True
        self.sensor2On = True


        if app is not None:
            self.callbacks()

    def layout(self) -> html.Div:
        refresh_interval = dcc.Interval(id="interval", interval=1000, n_intervals=0)

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
                {'label': 'Farenheit (F°)', 'value': 'F'},
                {'label': 'Celsius (C°)', 'value': 'C'},
            ],
            value="C",
        )

        dropdown_container = flex_builder(
            direction="row",
            children=[refresh_interval, temp_dropdown, time_dropdown],
            size="md",
        )  

        sensor_card_1 = self.tc1.render()
        sensor_card_2 = self.tc2.render()


        readings_chart = html.Div(id="line-chart")

        reading_flex = flex_builder(
            direction="row",
            children=[readings_chart],
            bordered=True
        )

        sensor_row_1 = flex_builder(
            direction="row",
            children=[
                sensor_card_1
            ]
        )

        sensor_row_2 = flex_builder(
            direction="row",
            children=[
                sensor_card_2
            ]
        )

        stats_flex = flex_builder(
            direction="column",
            children=[
                sensor_row_1,
                sensor_row_2
            ]
        )

        labels_flex = flex_builder(
            direction="row",
            children=[
                html.Div(self.sensor1Temperature, id="sensor1", style={"fontSize": "30px", "fontWeight": "bold"}),
                html.Div(self.sensor2Temperature, id="sensor2", style={"fontSize": "30px", "fontWeight": "bold"}),
            ],
            size="md",
        )


        visuals_row = flex_builder(
            direction="row",
            children=[
                reading_flex, stats_flex, labels_flex
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
            Input("interval", "n_intervals"),
        )
        def update_visuals(time_u, temp_u, _):

            # TODO get the global df from redis
            line_chart = create_chart(df=self.df, time_unit=time_u, temp_unit=temp_u)
            # todo, other charts: time, min, max, avg

            # Change the graph to reflect unit change
            if self.unit != temp_u:
                # Apply conversion to the temperature columns
                temperatureColumns = ["temperatureSensor1Data", "temperatureSensor2Data"]
                if temp_u == 'C':
                    self.df[temperatureColumns] = self.df[temperatureColumns].applymap(fahrenheitToCelsius)
                else:
                    self.df[temperatureColumns] = self.df[temperatureColumns].applymap(celsiusToFahrenheit)


            # Update the member variable
            self.unit = temp_u

            return line_chart

        @callback(
            Output("sensor1", "children"),
            Output("sensor2", "children"),
            Input("interval", "n_intervals") 
        )
        def update_labels(_):
            return self.sensor1Temperature, self.sensor2Temperature

    
    # Methods to change labels from outside
    def set_temp1_label(self, text: str):
        self.sensor1Temperature = text

    def set_temp2_label(self, text: str):
        self.sensor2Temperature = text

    
    