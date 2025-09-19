from dash import html, Output, Input, callback
import dash_ag_grid as dag
import pandas as pd

from database.db_methods import DB, User, Temperature

class SettingsPage:
    def __init__(self, db: DB):
        self.DB = db

    def layout(self) -> html.Div:
        users_df = self.DB.get_all_users()

        table = dag.AgGrid(
            rowData=users_df.to_dict(orient="records"),
            columnDefs=[{"field": i} for i in users_df.columns],
            id="dag-users"
        )

        return table

    @callback(
        Output("dag-users", "className"),
        Input("theme", "checked"),
    )
    def update_theme(switch_on):
        return "ag-theme-alpine-dark" if switch_on else "ag-theme-alpine"