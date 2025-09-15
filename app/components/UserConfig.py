from dash import html, callback, Output, Input
from components.builders import flex_builder, textbox_builder, toasty_button

class UserConfig:
    def __init__(self, app, config: dict):
        self.app = app
        self.config: dict = config
        self.id = self.config.get("id")
        self.config_row = []  

        self.curr_name = self.config.get("name")
        self.curr_phone_num = self.config.get("phone_num")
        self.curr_email_addr = self.config.get("email_addr")

        if app is not None:
            self.callbacks()

    def create(self):
        row = []
        for key, val in self.config.items():
            if key != "id":
                row.append(
                    textbox_builder(
                        label=key,
                        id=f"user-{self.id}-{key}",
                        value=val
                    )
                )

        btn = toasty_button(
            id=f"save-user-config-{self.id}",
            label="Save",
            disabled=True,
            toast_message=html.Div([
                html.Div(f"saving config for user: {self.id}"),
                html.Div(self.config)
            ], style={
                "display": "flex",
                  "flexDirection": "column"
                  }
            ),
            duration_ms=2000
        )
        row.append(btn)
        self.config_row = row

    def _layout(self):
        return html.Div(
            flex_builder(
                direction="row",
                children=self.config_row,
                bordered=True,
                justification="start",
                alignment="center"
            ),
            style={
                "width": "100%"
            }
        )

    def render(self):
        return html.Div(
            children=self._layout(),
            id=f"user-config-{self.id}"
        )

    def callbacks(self):
        @callback(
            Output(f"user-config-{self.id}", "children"),
            Output(f"save-user-config-{self.id}-toast", "is_open"),
            Output(f"save-user-config-{self.id}", "disabled"),
            Input(f"save-user-config-{self.id}", "n_clicks"),
            Input(f"user-{self.id}-name", "value"),
            Input(f"user-{self.id}-phone_num", "value"),
            Input(f"user-{self.id}-email_addr", "value"),
            prevent_initial_call=True
        )
        def update_config(n, name, phone_num, email_addr):
            print("----- HIT ------")
            # only let user submit if there is a change
            if name != self.curr_name or phone_num != self.curr_phone_num or email_addr != self.curr_email_addr:
                return self._layout(), False, True             

            # if there is a change and the user submits, then return to disabled state
            if n:
                print("SENDING TO DB:")
                print(f"name: {name}\nphone: {phone_num}\nemail: {email_addr}")
                self.curr_name = name
                self.curr_phone_num = phone_num
                self.curr_email_addr = email_addr

                # METHOD THAT UPDATES DB
                return self._layout(), True, False

            return self._layout(), True
