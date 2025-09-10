from dash import html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import random
import queue

class DashboardPage:
    def __init__(self, app):
        self.app = app

        self.temperatureData = queue.Queue()
        self.maxSize = 301

        for _ in range(self.maxSize):
            self.temperatureData.put(None)

        self.callbacks()

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
            html.Div(id='output', style={'marginTop': '20px'}), 

            dcc.Graph(id="graph"),

            dcc.Interval(
                id='interval-component',
                interval=1*1000,  # 1 second (1000 milliseconds)
                n_intervals=0
            )
        ])
    
    def callbacks(self):
        @callback(
            Output('output', 'children'),
            Input('dropdown', 'value')
        )
        def update_output(value):
            return f"You have selected: {value}"
        
        @callback(
            Output("graph", "figure"),
            Input("interval-component", "n_intervals"))
        def update_line_chart(dropdown_value):
            self.temperatureData.put(random.uniform(10,50))

            if self.temperatureData.qsize() > self.maxSize:
                self.temperatureData.get()

            temperatureData = pd.DataFrame({
                "seconds ago": list(range(self.maxSize)),
                "temperature": reversed(list(self.temperatureData.queue))
            })

            fig = px.line(temperatureData,
                x="seconds ago", y="temperature")
            fig.update_xaxes(autorange="reversed")
            return fig