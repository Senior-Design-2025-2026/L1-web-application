import dash_mantine_components as dmc
from dash import Dash, Output, Input, State, html, dcc, callback, MATCH
import dash_daq as daq
from dash_iconify import DashIconify
from utils.temperature_utils import get_heat_color
import uuid

class ThermostatCardAIO(html.Div):
    """
    - text: name of sensor 
    - aio_id: id name
    """
    class ids:
        segmented_control = lambda aio_id: {
            "component": "ThermostatCardAIO",
            "subcomponent": "segmented_control",
            "aio_id": aio_id
        }

        thermometer = lambda aio_id: {
            "component": "ThermostatCardAIO",
            "subcomponent": "thermometer",
            "aio_id": aio_id
        }

        value = lambda aio_id: {
            "component": "ThermostatCardAIO",
            "subcomponent": "value",
            "aio_id": aio_id
        }

        thermometer_div = lambda aio_id: {
            "component": "ThermostatCardAIO",
            "subcomponent": "thermometer_div",
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

        label = dmc.Text(
            self.text,
            size="xl",
            fw=700
        )

        # ======== SEGMENTED CONTROL ==========
        segmented_control = dmc.SegmentedControl(
            id=self.ids.segmented_control(aio_id),
            data=[
                {"value": "ON", "label": "ON"},
                {"value": "OFF", "label": "OFF"},
            ],
            value="ON",
            size="md"
        )

        # ============ THERMOMETER =========
        thermometer = html.Div(
            daq.Thermometer(
                id=self.ids.thermometer(aio_id),
                height=150,
                width=20,
            ),
            id=self.ids.thermometer_div(aio_id)
        )

        value = dmc.Text(
            id=self.ids.value(aio_id),
            size="xl",
            fz="h1",
            fw="500"
        )

        link_to_analytics = dmc.Anchor(
            href="https://engineering.uiowa.edu/",
            target="_blank",
            children=dmc.Center(
                [
                    dmc.Box("view analytics", ml=5),
                    DashIconify(
                        icon="tabler:arrow-right",
                        width=12,
                        height=12,
                    ),
                ],
                inline=True,
            ),
        )

        layout = dmc.Card(
            [
                # top: label and segment toggle
                dmc.CardSection(
                    dmc.Group(
                        [
                            label,
                            segmented_control
                        ],
                        align="center",
                        justify="space-between",
                        px="md",
                        py="sm"
                    ),
                    withBorder=True
                ),
                
                # middle: thermometer chart
                dmc.CardSection(
                    dmc.Group(
                        [
                            thermometer,
                            value
                        ],
                        justify="center",
                        align="center"
                    )
                ),

                # bottom: link to more stats
                dmc.CardSection(
                    dmc.Group(
                        [
                            link_to_analytics
                        ],
                        justify="end",
                        align="center",
                        px="md",
                        py="sm"
                    ),
                )
            ],
            withBorder=True,
            w=300
        )

        super().__init__(layout) 

    @callback(
        [
            # thermometer
            Output(ids.thermometer_div(MATCH), 'hidden'),
            Output(ids.thermometer(MATCH), 'value'),
            Output(ids.thermometer(MATCH), 'min'),
            Output(ids.thermometer(MATCH), 'max'),
            Output(ids.thermometer(MATCH), 'color'),
            # Output(ids.thermometer(MATCH), 'scale'),

            # reading
            Output(ids.value(MATCH), 'children'),
 
            # segment toggle
            Output(ids.segmented_control(MATCH), 'value'),
            Output(ids.segmented_control(MATCH), 'color'),
        ],
        [
            Input(ids.segmented_control(MATCH), 'value'),
            Input("theme", 'value'),
        ]
    )
    def update_thermostat_card(segment, checked):
        # TODO: stream to this and set the value depending on its physical state

        unit = "c"
        if unit == "c":
            thermometer_min = 0
            thermometer_max = 50

        elif unit == "f":
            thermometer_min = 32
            thermometer_max = 122

        color = "white" if checked else "black"

        scale = {
            'start': thermometer_min,
            'interval': 10,
            'end': thermometer_max,
        }


        # ON
        if segment == "ON":
            hidden = False
            thermometer_value = 30
            thermometer_color = get_heat_color(thermometer_value, "c")

            reading = "XXX °Y"

            segment_value = "ON"
            segment_color = "green"

        # OFF            
        else:
            hidden = True
            thermometer_value = 0
            thermometer_color = "#FFFFFF"

            reading = "N/A"

            segment_value = "OFF"
            segment_color = "red"

        

        return (
            hidden,
            thermometer_value,
            thermometer_min,
            thermometer_max,
            thermometer_color,
            # scale,

            reading,

            segment_value,
            segment_color
        )