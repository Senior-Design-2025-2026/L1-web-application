from dash import html, Output, Input, callback, ctx, State, no_update
import dash_ag_grid as dag
import os
import dash_mantine_components as dmc
from celery import Celery
from db.db_methods import DB

from components.new_user_form import new_user_form, new_user_form_defaults, new_user_form_no_updates, new_user_alert_props
# from components.update_user_form import update_user_form, update_user_form_defaults, update_user_form_no_updates, update_user_alert_props

class SettingsPage:
    def __init__(self, app, db: DB, celery: Celery):
        self.DB = db
        self.celery_client=celery

        if app is not None:
            self.callbacks()

    def layout(self) -> html.Div:
        new_user_modal_btn = dmc.Button(
                id="new-user-modal-btn",
                children=["Add User"]
        )

        new_user_modal_alert = dmc.Alert(
                id="new-user-alert",
                title="New User:",
                duration=2000,
                withCloseButton=True,
                hide=True,
            )

        users_df = self.DB.get_all_users()
        user_table = dag.AgGrid(
            rowData=users_df.to_dict(orient="records"),
            columnDefs=[{"field": i} for i in users_df.columns],
            id="dag-users"
        )

        return dmc.Stack(
            [
                new_user_modal_alert,
                new_user_modal_btn,
                user_table,
                new_user_form()
            ]
        )

    def callbacks(self):
        @callback(
            Output("new-user-modal", "opened"),

            Output("new-user-alert", "hide"),
            Output("new-user-alert", "color"),
            Output("new-user-alert", "children"),

            Output("new-user-min-thresh", "value"),
            Output("new-user-max-thresh", "value"),
            Output("new-user-email", "placeholder"),
            Output("new-user-email", "value"),
            Output("new-user-name", "placeholder"),
            Output("new-user-name", "value"),

            Input("new-user-submit", "n_clicks"),
            Input("new-user-cancel", "n_clicks"),
            Input("new-user-modal-btn", "n_clicks"),

            State("new-user-modal", "opened"),
            State("new-user-min-thresh", "value"),
            State("new-user-max-thresh", "value"),
            State("new-user-email", "value"),
            State("new-user-name", "value"),
            prevent_initial_call=True,
        )
        def new_user_modal(
            submit, 
            cancel,
            open,

            opened,
            min_thresh,
            max_thresh,
            email_addr,
            username
        ):
            trigger = ctx.triggered_id

            # open the modal
            if trigger == "new-user-modal-btn":
                return True, *(True, None,None), *new_user_form_defaults()

            # if user clicks submit button
            if trigger == "new-user-submit":

                # 1. check for fields
                fields = [min_thresh, max_thresh, email_addr, username]
                fields = [None if f=="" else f for f in fields]
                if any(f is None for f in fields):
                    error = "e1"
                    success = False

                # 2. check for uiowa email
                elif not email_addr.endswith("@uiowa.edu"):
                    error = "e2"
                    success = False

                # 3. basic checks passed; check for existence
                else:
                    exists = self.DB.does_email_exist(email_addr)
                    if not exists:
                        self.celery_client.send_task(
                            "add_user", 
                            kwargs={
                                "name":username,
                                "email_addr":email_addr,
                                "min_thresh_c":min_thresh,
                                "max_thresh_c":max_thresh,
                            }
                        )
                        error = ""
                        success = True
                    else:
                        error = "e3"
                        success = False

                if success:
                    return False, *new_user_alert_props("s"), *new_user_form_defaults()
                else:
                    return False, *new_user_alert_props(error), *new_user_form_no_updates()

            # cancel transaction
            if trigger == "new-user-cancel":
                return False, *(True, None, None), *new_user_form_defaults()

            else:
                return False, *(True, None, None), *new_user_form_no_updates()

        @callback(
            Output("dag-users", "className"),
            Input("theme", "checked"),
        )
        def update_theme(switch_on):
            color = "ag-theme-alpine-dark" if switch_on else "ag-theme-alpine"
            return color
