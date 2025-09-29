from dash import html, Output, Input, callback, ctx, State
import dash_ag_grid as dag
import os
import dash_mantine_components as dmc
from celery import Celery
from db.db_methods import DB
from components.user_form import new_user_form

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
            Input("new-user-submit", "n_clicks"),
            Input("new-user-cancel", "n_clicks"),
            Input("new-user-modal-btn", "n_clicks"),
            State("new-user-modal", "opened"),
            prevent_initial_call=True,
        )
        def new_user_modal(submit, cancel, open, opened):
            if ctx.triggered == "new-user-modal-btn":
                print("OPEN CLICKED")
            if ctx.triggered == "new-user-submit":
                print("SUBMIT CLICKED")
            if ctx.triggered == "new-user-cancel":
                print("CANCEL CLICKED")
            if ctx.triggered == "new-user-cancel":
                print("CANCEL CLICKED")

            return not opened
