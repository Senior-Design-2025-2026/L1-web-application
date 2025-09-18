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
        return dmc.Group(
            [
                ThermostatCardAIO("Sensor 1"),
                ThermostatCardAIO("Sensor 1"),
                ThermostatCardAIO("Sensor 2")
            ],
            justify="center",
            align="center"
        )

    