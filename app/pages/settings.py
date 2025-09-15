from dash import html

from components.builders import flex_builder
from components.UserConfig import UserConfig

class SettingsPage:
    def __init__(self, app):
        self.app = app

        if app is not None:
            self.callbacks()

    def get_dummy_users(self):
        # dummy user data for testing (AI gen-ed)
        users = [
            {"id": 1, "name": "Alice", "phone_num": "1234567890", "email_addr": "alice@example.com"},
            {"id": 2, "name": "Bob", "phone_num": "0987654321", "email_addr": "bob@example.com"},
        ]
        return users

    def layout(self) -> html.Div:
        users = self.get_dummy_users()
        user_configs = []

        for user in users:
            print("user:", user)
            user_config = UserConfig(self.app, user)
            user_configs.append(user_config.render())

        return flex_builder(
            direction="column",
            children=user_configs,
            alignment="start",
            justification="start"
        )
    
    def callbacks(self):
        ...