from dash import html, dcc, Output, Input, State

from components.builders import flex_builder
from components.UserConfig import UserConfig

def _walk_ids(component, path="root", found=None):
    if found is None:
        found = []
    # record this component if it has an id
    cid = getattr(component, "id", None)
    if cid is not None:
        found.append((path, type(component).__name__, cid))
    # dive into children
    children = getattr(component, "children", None)
    if isinstance(children, (list, tuple)):
        for idx, child in enumerate(children):
            _walk_ids(child, f"{path}.children[{idx}]", found)
    elif children is not None:
        _walk_ids(children, f"{path}.children", found)
    return found

class SettingsPage:
    def __init__(self, app):
        self.app = app
        self.saved_email = None
        self.max_temperature = 25
        self.register_callbacks()

    def register_callbacks(self):
        @self.app.callback(
            Output("saved-output", "children"),
            Input("save-email-button", "n_clicks"),
            State("max-temperature-input", "value"),
            State("email-input", "value")
        )
        def save_email(n_clicks, max_temp_value, email_value):
            if n_clicks > 0 and email_value:
                self.saved_email = email_value
                self.max_temperature = max_temp_value
                return f"Saved"
            return "No email saved yet"

    def get_dummy_users(self):
        users = [
            {"id": 1, "name": "Alice", "phone_num": "1234567890", "email_addr": "alice@example.com"},
            {"id": 2, "name": "Bob", "phone_num": "0987654321", "email_addr": "bob@example.com"},
        ]
        return users

    def layout(self) -> html.Div:
        users = self.get_dummy_users()
        self.user_configs = []
        self.user_data = []

        for user in users:
            user_config = UserConfig(self.app, user)
            user_config.create()
            div = user_config.render()
            self.user_configs.append(div)
            self.user_data.append(user)

        test = html.Div("test", id="TESTING")

        # Input field and button to save email
        email_input = dcc.Input(id="email-input", type="email", placeholder="Enter email")
        max_temperature_input = dcc.Input(id="max-temperature-input", type="number", placeholder="25")
        save_button = html.Button("Save", id="save-email-button", n_clicks=0)
        output_text = html.Div(id="saved-output")

        # Wrap them together
        email_section = html.Div([email_input, max_temperature_input, save_button, output_text])

        layout = flex_builder(
            direction="column",
            children=[email_section],
            alignment="start",
            justification="start"
        )
         
        return html.Div([
            test,
            layout
        ])