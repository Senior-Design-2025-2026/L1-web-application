from dash import html

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

    def get_dummy_users(self):
        users = [
            {"id": 1, "name": "Alice", "phone_num": "1234567890", "email_addr": "alice@example.com"},
            {"id": 2, "name": "Bob", "phone_num": "0987654321", "email_addr": "bob@example.com"},
        ]
        return users

    def layout(self) -> html.Div:
        users = self.get_dummy_users()
        self.user_configs = []

        for user in users:
            user_config = UserConfig(self.app, user)
            user_config.create()
            self.user_configs.append(user_config.render())

        test = html.Div("test", id="TESTING")

        print("++++++++++ ITEMS ++++++++++")
        for output, meta in self.app.callback_map.items():
            print("Output target:", output)
            print("Inputs:", [i["id"] for i in meta["inputs"]])
            print("State:", [s["id"] for s in meta["state"]])

        print("++++++++++ LAYOUT IDS (SettingsPage) ++++++++++")
        for path, comp_type, cid in _walk_ids(self):
            print(f"{path} :: {comp_type} :: id={cid}")

        layout = flex_builder(
            direction="column",
            children=self.user_configs,
            alignment="start",
            justification="start"
        )
         
        return html.Div([
            test,
            layout
        ])