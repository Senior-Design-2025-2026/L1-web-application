from dash import Dash, html, dcc, callback, Output, Input

class SettingsPage:
    def __init__(self, app):
        self.app = app

    def layout(self) -> html.Div:

        # here is an example of defining a html block and placing it within wanted dom position
        shitcoin = html.Div("MESSAGING SERVICE CONFIG")

        return html.Div(
            children=[
                html.Div(
                    "Settings page could contain some of the following",
                    style={
                        "font-weight":"bold"
                    }
                ),

                # using the predefined component
                shitcoin,

                html.Div(
                    "1. sms config"
                ),
                html.Div(
                    "2. sftp config"
                ),

                html.Div("OTHER CAPABILITIES"),
                html.Div("if we can nail the IPC between the embedded code and the web server, we should be able to easily change the data rate (assuming that the 1hz bound is per najeeb and not the temperature sensor)")
            ],
            # here is an example of inline css, however plotly dih lets you use .css file. This is super similar to inline html. 
            # THIS APPLIES TO THE PARENT DIV (because it is on the same level as the 'children' container)
            style={
                "display":"flex",
                "flex-direction":"column",
                "padding":"16px"
            }
        )