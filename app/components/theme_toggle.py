import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, Input, Output,  clientside_callback

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

theme_toggle = dmc.Switch(
    offLabel=DashIconify(icon="radix-icons:sun", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][8]),
    onLabel=DashIconify(icon="radix-icons:moon", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][6]),
    id="color-scheme-switch",
    persistence=True,
    color="grey",
)

app = Dash()

app.layout = dmc.MantineProvider(
    [theme_toggle, dmc.Text("Your page content")],
)

clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-switch", "id"),
    Input("color-scheme-switch", "checked"),
)