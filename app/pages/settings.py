from dash import html, Output, Input, callback, no_update
import dash_ag_grid as dag
import pandas as pd
import dash_mantine_components as dmc

from database.db_methods import DB, User, Temperature

class SettingsPage:
    def __init__(self, app, db: DB):
        self.DB = db

        if app is None:
            self.callbacks()

    def layout(self) -> html.Div:
        users_df = self.DB.get_all_users()
        table = dag.AgGrid(
            rowData=users_df.to_dict(orient="records"),
            columnDefs=[{"field": i} for i in users_df.columns],
            id="dag-users"
        )

        test_btn = dmc.Button(
            id="test-add",
            children="Test Add"
        )

        return dmc.Stack(children=[table, test_btn])

    def callbacks(self):
        @callback(
            Output("dag-users", "className"),
            Input("theme", "checked"),
        )
        def update_theme(switch_on):
            return "ag-theme-alpine-dark" if switch_on else "ag-theme-alpine"