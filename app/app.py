import dash
from dash import Dash, html, dcc, Input, Output, clientside_callback, _dash_renderer
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from pages.home import HomePage
from pages.dashboard import DashboardPage
from pages.settings import SettingsPage

from components.theme_toggle import theme_toggle
from components.header import header

# from db_conn.db_methods import DBConnection

# -------------- APP SETUP ------------ #
app = Dash(
    name="Lab1", 
    suppress_callback_exceptions=True, 
)


# ---------------- THEME ------------------ #
# Dash Mantine Components provides a light/ 
# dark mode context. Using default theme
# for simplicity...
theme={
    "primaryColor": "yellow",                          
    "defaultRadius": "sm",
    "components": {
        "Card": {
            "defaultProps": {
                "shadow": "xs"
            }
        }
    }
}

header = header()

# ---------------- DB CONNECTION ---------------- #
db_path = "app/db_conn/Lab1.db"
# db_conn = DBConnection(db_path=db_path)

# ----------------- APP ROUTING ----------------- #   
home_page_obj      = HomePage(app)
dashboard_page_obj = DashboardPage(app)
settings_page_obj  = SettingsPage(app)

app.layout = dmc.MantineProvider(
    [
        theme_toggle, 
        header,
        html.Div(id="page-content")
        # dmc.AppShell(
        #     [
        #         dmc.AppShellHeader(header),
        #         dmc.AppShellMain(id="page-content"),
        #     ],
        #     header={"height": 48},
        #     padding="md",
        #     id="appshell"
        # )
    ]
)

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    print("PATH", pathname)
    if pathname == '/' or pathname == '/home':
        return home_page_obj.layout()
    elif pathname == '/dashboard':
        return settings_page_obj.layout()
    elif pathname == '/config':
        return settings_page_obj.layout()
    else:
        return html.Div("404 Page Not Found")

if __name__ == '__main__':
    app.run(
        debug=True,
        port="8050",
        host="0.0.0.0"            
    )
