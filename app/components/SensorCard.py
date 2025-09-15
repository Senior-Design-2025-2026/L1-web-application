from dash import html, callback, Output, Input, no_update

from components.builders import flex_builder, toasty_button

class SensorCard:
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

    def create(self):
        btn_id = f"btn-sensor-{self._sensor_id}"
        text_id = btn_id + "-text"
        self.btn = toasty_button(
            id=btn_id,
            label=html.Div(id=text_id),
            toast_message=f"toggling sensor {self._sensor_id}",
            duration_ms=2000
        )
    
    def render(self):
        return html.Div(self.btn, id=f"temp-card-{self._sensor_id}")

    def _layout(self):
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

        return html.Div(
            flex_builder(
                direction="column",
                bordered=True,
                children=[
                    header,
                    reading,
                    self.btn,
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
            Output(f"temp-card-{self._sensor_id}", "children"),
            Output(f"btn-sensor-{self._sensor_id}-text", "children"),
            Output(f"btn-sensor-{self._sensor_id}-toast", "is_open"),
            Input(f"btn-sensor-{self._sensor_id}", "n_clicks"),
        )
        def render(n):
            if n == 0:
                # method to get the current status from redis
                # for now set on
                return self._layout(), "Turn Off", False
            elif n and self._active:
                self.turn_off()
                return self._layout(), "Turn On", True
            elif n and not self._active:
                self.turn_on()
                return self._layout(), "Turn Off", True