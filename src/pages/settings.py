from dash import html, Output, Input, callback, ctx, State, no_update
import redis
import dash_ag_grid as dag
import os
import dash_mantine_components as dmc
from celery import Celery
from dash_iconify import DashIconify

from db.db_methods import DB
from components.new_user_form import new_user_form, new_user_form_defaults, new_user_form_no_updates, new_user_alert_props
from components.update_user_form import get_no_update_fields, update_user_form, get_user_fields, update_user_alert_props

class SettingsPage:
    def __init__(self, app, db: DB, redis, celery):
        self.DB = db
        self.red = redis
        self.celery_client=celery

        if app is not None:
            self.callbacks()

    def layout(self) -> html.Div:
        # buttons
        new_user_modal_btn = dmc.Button(
                id="new-user-modal-btn",
                children=["Add User"],
                leftSection=DashIconify(icon="qlementine-icons:new-16"),
                color="green"
        )

        update_user_modal_btn = dmc.Button(
                id="update-user-modal-btn",
                children=["Edit User"],
                leftSection=DashIconify(icon="cuida:edit-outline"),
        )

        btn_group = dmc.Group(
            [
                new_user_modal_btn,
                update_user_modal_btn
            ],
            justify="flex-end",
            align="center"
        )

        # alerts
        new_user_modal_alert = dmc.Alert(
                id="new-user-alert",
                title="New User:",
                duration=2000,
                withCloseButton=True,
                hide=True,
            )

        update_user_modal_alert = dmc.Alert(
                id="update-user-alert",
                title="Update User",
                duration=2000,
                withCloseButton=True,
                hide=True,
            )

        # user table
        users_df = self.DB.get_all_users()
        user_table = dag.AgGrid(
            rowData=users_df.to_dict(orient="records"),
            columnDefs=[{"field": i} for i in users_df.columns],
            id="dag-users"
        )

        return dmc.Stack(
            [
                new_user_modal_alert,
                update_user_modal_alert,
                dmc.Group(
                    [
                        dmc.Title("Settings"),
                        btn_group,
                    ],
                    justify="space-between",
                    align="center"
                ),
                user_table,
                new_user_form(),   # hidden modal
                update_user_form() # hidden modal
            ]
        )

    def callbacks(self):

        # ====================================
        #             THEME TOGGLE
        # ====================================
        @callback(
            Output("dag-users", "className"),
            Input("theme", "checked"),
        )
        def update_theme(switch_on):
            color = "ag-theme-alpine-dark" if switch_on else "ag-theme-alpine"
            return color

        # ====================================
        #             NEW USER FORM
        # ====================================
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

    # ====================================
    #           UPDATE USER FORM 
    # ====================================
        @callback(
            # modal state
            Output("update-modal-stack", "opened"),
            Output("update-modal-stack", "closeAll"),

            # alert props
            Output("update-user-alert", "hide"),
            Output("update-user-alert", "color"),
            Output("update-user-alert", "children"),

            # output of email selected (load from redis)
            Output("update-select-email", "value"),

            # output field states (based on email selected)
            Output("update-user-min-thresh", "value"),
            Output("update-user-max-thresh", "value"),
            Output("update-user-email", "value"),
            Output("update-user-name", "value"),

            # modal control
            Input("update-user-submit", "n_clicks"),
            Input("confirm-submit-user-update", "n_clicks"),
            Input("update-user-cancel", "n_clicks"),
            Input("confirm-cancel-user-update", "n_clicks"),

            # open button
            Input("update-user-modal-btn", "n_clicks"),

            # email dropdown
            Input("update-select-email", "value"),

            # new field states
            State("update-user-min-thresh", "value"),
            State("update-user-max-thresh", "value"),
            State("update-user-email", "value"),
            State("update-user-name", "value"),
            prevent_initial_call=True,
        )
        def update_user_modal(
            submit, 
            confirm, 
            cancel,
            cancel_confirm, 

            open,

            update_select_email,

            min_thresh,
            max_thresh,
            email_addr,
            username
        ):
            trigger = ctx.triggered_id
            if trigger == "update-user-model-btn":
                print("OPENED")
                # something with the redis cache
                # to set default
                open = "update-user-modal"
                close_all = False
                alert_props = update_user_alert_props("")
                fields = get_no_update_fields()
                return open, close_all, *alert_props, None, *fields

            if trigger == "update-select-email":
                print("OPENED")
                # something with the redis cache
                # to change the field values
                open = "update-user-modal"
                close_all = False
                alert_props = update_user_alert_props("")
                fields = get_no_update_fields()
                return open, close_all, *alert_props, None, *fields

            if trigger in ("update-user-cancel", "confirm-cancel-user-update"):
                print("CLOSED")
                open = None
                close_all = True
                alert_props = update_user_alert_props("")
                fields = get_no_update_fields()
                return open, close_all, *alert_props, None, *fields

            if trigger == "update-user-submit":
                print("SUBMITTED")
                open = None
                close_all = True
                alert_props = update_user_alert_props("")
                fields = get_no_update_fields()
                return open, close_all, *alert_props, None, *fields

            else:
                alert_props = update_user_alert_props("")
                fields = get_no_update_fields()
                return no_update, no_update, *alert_props, None, *fields
