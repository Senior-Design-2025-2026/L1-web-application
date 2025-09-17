import dash_mantine_components as dmc
from dash import Dash, Output, Input, State, html, dcc, callback, MATCH
import uuid

class ThermostatCardAIO(html.Div):
    """
    - text: name of sensor 
    - aio_id: id name
    """
    class ids:
        button = lambda aio_id: {
            "component": "ThermostatCardAIO",
            "subcomponent": "button",
            "aio_id": aio_id
        }

        temperature = lambda aio_id: {
            "component": "ThermostatCardAIO",
            "subcomponent": "temperature",
            "aio_id": aio_id
        }

        indicator = lambda aio_id: {
            "component": "ThermostatCardAIO",
            "subcomponent": "indicator",
            "aio_id": aio_id
        }

    ids = ids

    def __init__(
            self,
            text,
            aio_id=None
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())
        
        self.text = text

        super().__init__([
            html.Div(f"sensor {text}"),
            html.Div(id=self.ids.button(aio_id)),
            html.Div(id=self.ids.temperature(aio_id)),
            html.Div(id=self.ids.indicator(aio_id)),
            html.Div(
                f"aio test with button id: {self.ids.button(aio_id).get("aio_id")}, "
                f"temp id: {self.ids.temperature(aio_id).get("aio_id")}, "
                f"indicator id: {self.ids.indicator(aio_id).get("aio_id")}"
            ),
        ]) 
    # @callback(
    #     [
    #         Output(ids.button(MATCH), 'children'),
    #         Output(ids.temperature(MATCH), 'children'),
    #         Output(ids.indicator(MATCH), 'value'),
    #     ],
    #     [
    #         Input(ids.button(MATCH), 'children'),
    #         Input("system-clock", "n_intervals")
    #     ]
    # )
    # def update_thermostat_card(color, existing_style):
    #     card = dmc.Card(
    #         [
    #             # header: sensor id + on/off inication
    #             dmc.CardSection(
    #                 dmc.Group(
    #                     [
    #                         dmc.Text(
    #                             ""
    #                         )

    #                     ]
    #                 )
    #             )
    #         ]

    #     )

    #     return existing_style