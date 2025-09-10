from dash import Dash, html, dcc, callback, Output, Input

class DashboardPage:
    def __init__(self, app):
        self.app = app

    def layout(self) -> html.Div:
        return html.Div([
            html.H1("Dashboard Page"),
            
            # dropdown example 
            # the way this works is by listening to a change value of id 'dropdown'
            # see callback below...
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'Option 1', 'value': 'option1'},
                    {'label': 'Option 2', 'value': 'option2'},
                    {'label': 'Option 3', 'value': 'option3'}
                ],
                value='option1',
                placeholder="Select an option"
            ),

            # stores the output from the callback (current dropdown val)
            html.Div(id='output', style={'marginTop': '20px'})
        ])
    
    def callbacks(self):
        @callback(
            Output('output', 'children'),
            Input('dropdown', 'value')
        )
        def update_output(value):
            return f"You have selected: {value}"