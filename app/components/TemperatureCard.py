from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc

from components.flex_builder import flex_builder

class TemperatureCard():
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

        toggle_button = dbc.Button(
            html.Div(id=f"btn-text-{self._sensor_id}"),
            id=f"toggle-button-{self._sensor_id}",
            outline=True,
            color="success"
        )

        card = flex_builder(
            direction="column",
            bordered=True,
            children=[
                header,
                reading,
                toggle_button,
            ],
            justification="space-between",
            alignment="center"
        )
         
        return card

    def callbacks(self):
        @callback(
            Output(f"temp-card-{self._sensor_id}", "children", allow_duplicate=True),
            Output(f"btn-text-{self._sensor_id}", "children"),
            Output(f"toggle-button-{self._sensor_id}", "color"),
            Input(f"toggle-button-{self._sensor_id}", "n_clicks"),
            prevent_initial_call=True
        )
        def toggle_active(n_clicks):
            if n_clicks and self._active:
                self.turn_off()
                text = "Turn On"
                # color = "success"
            else:
                self.turn_on()
                text = "Turn Off"
                # color = "danger"

            color = "secondary"

            return self.render(), text, color 