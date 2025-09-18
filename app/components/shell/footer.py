import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Output, Input, callback, html, get_asset_url
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output,  clientside_callback

def footer():
    # class_notice = dmc.Center(
    #     [
    #         dmc.Text(
    #             "Principles of ECE/CSE Design Fall 2025",
    #             fz="md",
    #         ),
    #         dmc.Text(
    #             "•",
    #             style={
    #                 "marginLeft": "0.5em",
    #                 "marginRight": "0.5em"
    #             }
    #         ),
    #         dmc.Text(
    #             "Labratory 1",
    #             fz="md"
    #         ),
    #     ]
    # )

    return dmc.Stack(
        [
            html.Div(
                [
                    DashIconify(
                        icon="mdi:heart-outline",
                        color="red",
                        width=14
                    ),
                    dmc.Text(
                        "Dashboard Created by Team 3",
                        fz="sm",
                        style={
                            "font-style": "italic",
                        },
                    ),
                ],
                style={
                    "display":"flex",
                    "gap": "0.5em",
                    "align-items": "center"
                }
            ),
            dmc.Center(
                dmc.Anchor(
                    href="https://engineering.uiowa.edu/",
                    target="_blank",
                    children=dmc.Center(
                        [
                            dmc.Box("University of Iowa, College of Engineering", ml=5),
                            DashIconify(
                                icon="lsicon:export-filled",
                                width=12,
                                height=12,
                            ),
                        ],
                        inline=True,
                    ),
                )
            )
        ],
        justify="center",
        align="center",
        style={
            "display":"flex",
            "flex-direction":"column",
            "margin": "1em"
        }
    )