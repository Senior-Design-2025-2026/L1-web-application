import dash_mantine_components as dmc
from dash import Dash, Output, Input, State, html, dcc, callback, MATCH, ctx
import dash_daq as daq
from dash_iconify import DashIconify
from utils.temperature_utils import c_to_f, c_to_k
import uuid

RANGE_C = [0, 10, 20, 30, 40, 50]           # hardcoded... this is verified
RANGE_F = [32, 50, 68, 86, 104, 122]
RANGE_K = [273, 283, 293, 303, 313, 323]

class ThermostatCardAIO(html.Div):
    class ids:
        data = lambda aio_id: {
            "component": "ThermostatCardAIO",
            "subcomponent": "data",
            "aio_id": aio_id
        }

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
            aio_id=None,
            color="red",
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # ======== CARD TITLE ======== 
        label = dmc.Text(
            text,
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
                color=color

            ),
            id=self.ids.thermometer_div(aio_id)
        )

        value = dmc.Text(
            id=self.ids.value(aio_id),
            size="xl",
            fz="h1",
            fw="500"
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
                            dcc.Store(id=self.ids.data(aio_id)),
                            thermometer,
                            value
                        ],
                        justify="center",
                        align="center",
                        h="200px",
                        mb="30"
                    )
                ),
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
            Output(ids.thermometer(MATCH), 'scale'),

            # reading
            Output(ids.value(MATCH), 'children'),
 
            # segment toggle
            Output(ids.segmented_control(MATCH), 'value'),
            Output(ids.segmented_control(MATCH), 'color'),
        ],
        [
            Input(ids.segmented_control(MATCH), 'value'),
            Input("theme", "checked"),
            Input("unit-dropdown", "value"),
            Input(ids.data(MATCH), "data"),
        ]
    )
    def update_thermostat_card(segment, checked, unit, data):
        if data:
            temp = float(data.get("val"))

        # range
        if unit == "c":
            range = RANGE_C
        elif unit == "k":
            range = RANGE_K
        elif unit == "f":
            range = RANGE_F

        thermometer_min = range[0]
        thermometer_max = range[-1]
        
        # scale 
        scale_color = "#C9C9C9" if checked else "#454545"   
        thermometer_scale = {
            "custom": {
                val: {"label": str(val), "style": {"color": scale_color}}
                for val in range
            }
        }

        # IF ON: display
        if segment == "ON":
            hidden = False

            if unit == "f":
                temp = c_to_f(temp)
                unit = f" °{unit.upper()}"
            elif unit == "k":
                temp = c_to_k(temp)
                unit = "K"
            else:
                unit = f" °{unit.upper()}"

            reading = f"{temp}{unit}"

            segment_value = "ON"
            segment_color = "green"

        # IF OFF: display message
        else:
            hidden = True
            thermometer_value = 0

            reading = "N/A"

            segment_value = "OFF"
            segment_color = "red"

        return (
            hidden,
            temp,
            thermometer_min,
            thermometer_max,
            thermometer_scale,

            reading,

            segment_value,
            segment_color
        )