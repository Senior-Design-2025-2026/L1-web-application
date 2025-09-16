import dash
from dash import Dash, html, dcc, Input, Output, clientside_callback, _dash_renderer
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from pathlib import Path

from pages.home import HomePage
from pages.analytics import analyticsPage
from pages.configuration import configurationPage

from components.header import header
from components.theme_toggle import theme_toggle

# from db_conn.db_methods import DBConnection

# -------------- APP SETUP ------------ #
app = Dash(
    name="Lab1", 
    assets_folder=str(Path.cwd() / "app" / "assets")
)

header = header()

# ---------------- DB CONNECTION ---------------- #
db_path = "app/db_conn/Lab1.db"
# db_conn = DBConnection(db_path=db_path)

# ----------------- APP ROUTING ----------------- #   
home_page_obj      = HomePage(app)
analytics_page_obj = AnalyticsPage(app)
configuration_page_obj  = ConfigurationPage(app)

app.layout = dmc.MantineProvider(
    children=[
        dcc.Location(id='url'),
        dmc.AppShell(
            [
                dmc.AppShellHeader(header),
                dmc.AppShellMain(html.Div(id="page-content"))
            ],
            header={"height":60, "width":"100%"}
        )
    ],
)

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    print("PATH", pathname)
    if pathname == '/' or pathname == '/home':
        return home_page_obj.layout()
    elif pathname == '/analytics':
        return analytics_page_obj.layout()
    elif pathname == '/configuration':
        return configuration_page_obj.layout()
    else:
        return html.Div("404 Page Not Found")

if __name__ == '__main__':
    app.run(
        debug=True,
        port="8050",
        host="0.0.0.0"            
    )
