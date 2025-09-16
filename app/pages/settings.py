from dash import html

class SettingsPage:
    def __init__(self, app):
        self.app = app

    def layout(self) -> html.Div:
        return html.Div("settings")
    