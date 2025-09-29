from dash import html, Output, Input, callback, ctx, State, no_update
import dash_ag_grid as dag
import os
import dash_mantine_components as dmc
from celery import Celery
from db.db_methods import DB

from components.user_form import new_user_form, new_user_form_defaults, new_user_form_no_updates

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

        return dmc.Stack(
            [
                new_user_modal_btn,
                new_user_form()
            ]
        )

    def callbacks(self):
        @callback(
            Output("new-user-modal", "opened"),

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
                return True, *new_user_form_defaults()

            # if user clicks submit button
            if trigger == "new-user-submit":
                print("SUBMIT CLICKED")

                # check for existence of username (pk)

                # add user to the database
                # if there is an error, raise toast
                success = True
                if success:
                    return False, *new_user_form_defaults()
                else:
                    return True, *new_user_form_no_updates()

            # cancel transaction
            if trigger == "new-user-cancel":
                print("CANCEL CLICKED")
                return False, *new_user_form_defaults()

            else:
                return False, *new_user_form_no_updates()

