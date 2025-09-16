from dash import html

class SettingsPage:
    def __init__(self, app):
        self.app = app

    def __init__(self, app):
        self.app = app

        if app is not None:
            self.callbacks()

    def layout(self) -> html.Div:
        ...
    
    def callbacks(self):
        ...