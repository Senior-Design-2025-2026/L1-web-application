from ctypes import alignment
from dash import html, Output, Input, callback, ctx
import dash_ag_grid as dag
import os
import dash_mantine_components as dmc

def new_user_form():
    # name
    form_name = dmc.TextInput(
        label="Username",
        w=200
    )

    # email
    form_email = dmc.TextInput(
        label="Email Address",
        w=200
    )

    # threshold min
    form_min_threshold_c = dmc.NumberInput(
        label="Minimum Threshold (°C)",
        min=0,
        max=50,
        value=10,
        step=1,
        w=200
    ) 

    # threshold max
    form_max_threshold_c = dmc.NumberInput(
        label="Maximum Threshold (°C)",
        min=0,
        max=50,
        value=30,
        step=1,
        w=200
    ) 

    threshold_row = dmc.Group(
        [
            form_min_threshold_c, form_max_threshold_c
        ],
        align="center",
        justify="space-between"
    )

    submit_button = dmc.Button(
        id="new-user-submit",
        children=["Submit User"],
        color="green"
    )

    cancel_button = dmc.Button(
        id="new-user-cancel",
        children=["Cancel"],
        color="red",
        variant="outline"
    )

    button_row = dmc.Group(
        [
            submit_button, 
            cancel_button
        ], 
        justify="flex-end"
    )

    form = dmc.Stack(
        [
            form_name,
            form_email,
            threshold_row,
            button_row
        ]
    )

    modal = dmc.Modal(
        title="New User",
        id="new-user-modal",
        children=[
            form        
        ]
    )

    return modal
