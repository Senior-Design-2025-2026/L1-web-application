from dash import html
from database.db_methods import DB

class AnalyticsPage:
    def __init__(self, app, db: DB):
        self.DB = db

        if app is None:
            self.callbacks()

    def layout(self) -> html.Div:
        return html.Div("dashboard")

    def callbacks(self):
        ...