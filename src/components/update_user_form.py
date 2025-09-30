from ctypes import alignment
from dash import html, Output, Input, callback, ctx, no_update
from dash_iconify import DashIconify
import dash_ag_grid as dag
import os
import dash_mantine_components as dmc
import pandas as pd

# forms are a perfect use case for dash all in one components
# whoops

def get_user_fields(row: pd.DataFrame) -> tuple:
    name       = row.iloc[0]["name"]
    email_addr = row.iloc[0]["email_addr"]
    min_thresh = row.iloc[0]["min_thresh_c"]
    max_thresh = row.iloc[0]["max_thresh_c"]

    return (name, email_addr, min_thresh, max_thresh)

def get_no_update_fields() -> tuple:
    name       = no_update
    email_addr = no_update    
    min_thresh = no_update
    max_thresh = no_update

    return (name, email_addr, min_thresh, max_thresh)

def update_user_alert_props(alert_type:str) -> tuple:
    if alert_type == "e1":
        return (False, "red", "Error: one or more inputs are empty")
    elif alert_type == "e2":
        return (False, "red", "Error: a non-uiowa edu email was inputted")
    elif alert_type == "e3":
        return (False, "red", "Error: email already exists")
    elif alert_type == "s":
        return (False, "green", "Success: user added!")
    else:
        return (True, None, None)

def update_user_form():
    # email (this drives the other fields)
    select_email = dmc.Select(
        id="update-select-email",
        label="User Email",
        searchable=True,
    )

    # name
    form_name = dmc.TextInput(
        id="update-user-name",
        label="Name",
    )

    # email
    form_email = dmc.TextInput(
        id="update-user-email",
        label="Email",
        description="Must be a University of Iowa email (@uiowa.edu)",
    )

    # threshold min
    form_min_threshold_c = dmc.NumberInput(
        id="update-user-min-thresh",
        label="Minimum Threshold (°C)",
        min=0,
        max=50,
        step=1,
    ) 

    # threshold max
    form_max_threshold_c = dmc.NumberInput(
        id="update-user-max-thresh",
        label="Maximum Threshold (°C)",
        min=0,
        max=50,
        step=1,
    ) 

    threshold_row = dmc.Group(
        [
            form_min_threshold_c, form_max_threshold_c
        ],
        align="center",
        justify="space-between",
    )

    submit_button = dmc.Button(
        id="update-user-submit",
        children=["Submit Changes"],
        color="green"
    )

    cancel_button = dmc.Button(
        id="update-user-cancel",
        children=["Cancel"],
        color="red",
        variant="outline"
    )

    button_row = dmc.Group(
        [
            submit_button, 
            cancel_button
        ], 
        justify="flex-end",
        mt="md"
    )

    form = dmc.Stack(
        [
            select_email,
            form_name,
            form_email,
            threshold_row,
            button_row
        ]
    )

    title = dmc.Center(
        [
            DashIconify(icon="fa7-solid:user-edit", width=30),
            dmc.Text("update User", fz="h3", ml="md"),
        ]
    )

    modal = dmc.ModalStack(
        id="update-modal-stack",
        children=[
            dmc.ManagedModal(
                id="update-user-modal",
                title=title,
                children=[
                    form
                ],
            ),
            dmc.ManagedModal(
                id="confirm-update-user",
                title="Confirm Update",
                children=[
                    dmc.Text(id="confirm-update-pending-changes"),
                    dmc.Group(
                        children=[
                            dmc.Button("Confirm", id="confirm-submit-user-update", color="green"),
                            dmc.Button("Cancel", id="confirm-cancel-user-update", color="red", variant="outline"),
                        ],
                        mt="md",
                        justify="flex-end",
                    )
                ]
            )
        ]
    )

    return modal
