from dash import html, Output, Input, callback, ctx
import dash_ag_grid as dag
import dash_mantine_components as dmc

from database.db_methods import DB

class SettingsPage:
    def __init__(self, app, db: DB):
        self.DB = db

        if app is not None:
            self.callbacks()

    def layout(self) -> html.Div:
        temps = self.DB.get_all_temperatures()
        temp_table = dag.AgGrid(
            rowData=temps.to_dict(orient="records"),
            columnDefs=[{"field": i} for i in temps.columns],
            id="dag-users"
        )

        users_df = self.DB.get_all_users()
        user_table = dag.AgGrid(
            rowData=users_df.to_dict(orient="records"),
            columnDefs=[{"field": i} for i in users_df.columns],
            id="dag-users"
        )

        test_btn = dmc.Button(
            id="test-add",
            children="Test Add"
        )

        return dmc.Stack(children=[temp_table, user_table, test_btn, html.Div(id="empty")])

    def callbacks(self):
        @callback(
            Output("dag-users", "className"),
            Input("theme", "checked"),
        )
        def update_theme(switch_on):
            return "ag-theme-alpine-dark" if switch_on else "ag-theme-alpine"

        @callback(
            Output("empty", "children"),
            Input("test-add", "n_clicks"),
        )
        def test_add(n_clicks):
            if ctx.triggered_id == "test-add":          
                self.DB.add_user(name="test", phone_num="add", email_addr="user")