from dash import html
import dash_bootstrap_components as dbc

from components.builders import flex_builder

def footer(project_links: dict = None, linkedIn_links: dict = None):
    def link_row(links: dict):
        row = []

        for key, val in links.items():
            link = dbc.NavLink(key, href=val, external_link= 'True', target='_blank', style={"color":"#454545", "text-decoration":"underline"})
            row.append(link)

        return row

    project_links = link_row(project_links)
    linkedIn_links = link_row(linkedIn_links)

    layout = html.Div(
        flex_builder(
            direction="column",
            children=[
                html.Div("Lab 1: Senior Design", style={"font-weight":"bold", "font-size":"20px"}),

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
        style={
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "boxShadow": "0 -4px 6px rgba(0, 0, 0, 0.1)",  
            "padding": "10px",
            "backgroundColor": "#c7c6c5"

        },
    )

    return layout

        