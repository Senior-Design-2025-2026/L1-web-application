from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc

from components.builders import flex_builder, toasty_button

class TemperatureCard:
    def __init__(self, app, sensor_id: int):
        self._sensor_id = sensor_id
        self._active = True
        self._temperature = None
        self._unit = "f"

        if app is not None:
            self.callbacks()

    def set_unit(self, unit: str):
        self._unit = unit

    def turn_on(self):
        self._active = True

    def turn_off(self):
        self._active = False

    def get_temp(self):
        return self._temperature

    def update(self, message: dict):
        # todo, push to database
        self._temperature = message.get("temp")

    def render(self) -> html.Div:
        label = html.Div(
            f"Sensor: {self._sensor_id}",
            style={
                "color": "#454545",
                "font-weight": "bold"
            }
        )

        active_indicator = html.Div(
            style={
                "width": "12px",
                "height": "12px",
                "border-radius": "20px",
                "background-color": "green" if self._active else "red"
            }
        )

        header = flex_builder(
            direction="row",
            children=[label, active_indicator],
            justification="space-between",
            alignment="center"
        )

        reading = html.Div(
            (str(self._temperature) + self._unit + "°") if self._active and self._temperature is not None else "Sensor Inactive",
            style = {
                "font-size": "xlarge",
                "font-weight": "bolder",
                "color": "#454545"
            }
        )

        id = f"btn-sensor-{self._sensor_id}"
        toggle_button = toasty_button(
            id=id,
            label=html.Div(
                id=(id+"-text")
            ),
            toast_message=f"toggling sensor {self._sensor_id}"
        )

        return html.Div(
            flex_builder(
                direction="column",
                bordered=True,
                children=[
                    header,
                    reading,
                    toggle_button,
                ],
                justification="space-between",
                alignment="center"
            ),
            style={
                "width":"100%", 
                "height":"100%"
            }
        )

    def callbacks(self):
        @callback(
            Output(f"btn-sensor-{self._sensor_id}", "children", allow_duplicate=True),
            Output(f"btn-sensor-{self._sensor_id}-text", "children"),
            Input(f"btn-sensor-{self._sensor_id}", "n_clicks"),
            prevent_initial_call=True
        )
        def toggle_active(n_clicks):
            print("TESTTEST")
            if n_clicks and self._active:
                self.turn_off()
                text = "Turn On"
            else:
                self.turn_on()
                text = "Turn Off"

            return self.render(), text