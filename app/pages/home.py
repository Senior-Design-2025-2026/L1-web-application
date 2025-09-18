from dash import html
import dash_mantine_components as dmc

from components.aio.thermostat_card import ThermostatCardAIO

class HomePage:
    def __init__(self, db: str = None):
        self.db = None

    def layout(self):
        # TODO:
        # Home Page should consist of 2 simple visuals  
        #   on laptop: flex horiz
        #   on phone: flex vert
        # These are cards with thermometers 
        # within the button there should be an indicator for off/on
        # card has action button to expand to a larger visuals?
        cards = dmc.Stack(
            [
                ThermostatCardAIO("Sensor 1"),
                ThermostatCardAIO("Sensor 1"),
            ],
            justify="center",
            align="center"
        )


        data = [
            {"date": "Mar 22", "Apples": 2890, "Oranges": 2338, "Tomatoes": 2452},
            {"date": "Mar 23", "Apples": 2756, "Oranges": 2103, "Tomatoes": 2402},
            {"date": "Mar 24", "Apples": 3322, "Oranges": 986, "Tomatoes": 1821},
            {"date": "Mar 25", "Apples": 3470, "Oranges": 2108, "Tomatoes": 2809},
            {"date": "Mar 26", "Apples": 3129, "Oranges": 1726, "Tomatoes": 2290}
        ]

        line_chart = dmc.Card(
            dmc.LineChart(
                h=300,
                w=500,
                dataKey="date",
                data=data,
                series = [
                    {"name": "Apples", "color": "indigo.6"},
                    {"name": "Oranges", "color": "blue.6"},
                    {"name": "Tomatoes", "color": "teal.6"}
                ],
                curveType="Linear",
                tickLine="y",
                gridAxis="x",
                withXAxis="True",
                withYAxis="True",
                withDots="True",
            )
        )

        home = dmc.Group(
            [
                cards,
                line_chart
            ]
        )

        return home



    