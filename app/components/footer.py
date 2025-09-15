from dash import html
import dash_bootstrap_components as dbc

from components.builders import flex_builder

def footer(project_links: dict = None, linkedIn_links: dict = None):
    def link_row(links: dict):
        row = []

        for key, val in links.items():
            link = dbc.NavLink(key, href=val, className="link")
            row.append(link)

        return row

    project_links = link_row(project_links)
    linkedIn_links = link_row(linkedIn_links)

    layout = html.Div(
        flex_builder(
            direction="column",
            children=[
                html.Div("Lab 1: Senior Design"),

                # linked ins
                flex_builder(
                    direction="row",
                    children=linkedIn_links,
                    alignment="center",
                    justification="center"
                ),

                # project links
                flex_builder(
                    direction="row",
                    children=project_links,
                    alignment="center",
                    justification="center"
                ),
            ],
        ), 
        className="footer"
    )

    return layout

        