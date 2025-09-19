from dash import html

from database.db_methods import DB, User, Temperature

class AnalyticsPage:
    def __init__(self, db: DB):
        self.DB = db

    def layout(self) -> html.Div:
        return html.Div("dashboard")