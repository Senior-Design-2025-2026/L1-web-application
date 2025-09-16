from dash import html
import dash_bootstrap_components as dbc

from components.builders import flex_builder

def footer(project_links: dict = None, linkedIn_links: dict = None):
    def link_col(links: dict, label: str):
        col = []

        col.append(html.Div(label, style={"font-size":"16px", "font-weight":"bold"}))

        for key, val in links.items():
            link = dbc.NavLink(key, href=val, external_link= 'True', target='_blank', style={"color":"#454545", "text-decoration":"underline"})
            col.append(link)

        return col

    project_links = link_col(project_links, "Project Docs")
    linkedIn_links = link_col(linkedIn_links, "LinkedIns")

    layout = html.Div(
        [
        flex_builder(
            direction="row",
            children=[
                flex_builder(
                    direction="column",
                    children=linkedIn_links,
                    alignment="start",
                    justification="start"
                ),
                flex_builder(
                    direction="column",
                    children=project_links,
                    alignment="start",
                    justification="start"
                ),
            ],
            justification="center",
            alignment="center"
        ), 
    ],
        style={
            "display": "flex",
            "flex-direction":"column",
            "justify-content": "center",
            "align-items": "center",
            "padding": "10px",
            "backgroundColor": "#dedede"
        },
    )

    return layout

        