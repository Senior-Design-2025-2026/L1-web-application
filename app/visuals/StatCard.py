from dash import html, callback
from dash.dependencies import Input, Output

from utils.conversions import c_to_f
from components.builders import flex_builder

class StatCard:
    def __init__(self, app, sensor_id: int, field: str = "temperature", stat_method: str = "avg", test_df=None):
        self.app = app
        self.sensor_id = sensor_id
        self.field = field
        self.stat_method = stat_method
        self.reading = None  
        self.test_df = test_df

        if app is not None:
            self.callbacks()

    def create(self):
        return html.Div(id=f"temp-card-{self.sensor_id}-{self.field}-{self.stat_method}")

    def calculate_stat(self, df):
        print(f"calculating for {self.stat_method}")
        if self.stat_method in ["average", "avg"]:
            print("mean")
            val = df.loc[:, self.field].mean()
        elif self.stat_method in ["minimum", "min"]:
            print("min")
            val = df.loc[:, self.field].min()
        elif self.stat_method in ["maximum", "max"]:
            print("max")
            val = df.loc[:, self.field].max()
        else:
            raise ValueError(f"Unsupported stat_method: {self.stat_method}")
        
        print(val)
        return val

    def _layout(self, val):
        label = html.Div(
            f"{str(self.stat_method).capitalize()} {str(self.field).capitalize()}:",
            style={
                "color": "#454545",
                "font-weight": "bold"
            }
        )

        reading = html.Div(
            val,
            style = {
                "font-size": "xlarge",
                "font-weight": "bolder",
                "color": "#454545"
            }
        )

        return html.Div(
            flex_builder(
                direction="column",
                bordered=True,
                children=[
                    label,
                    reading,
                ],
                justification="space-between",
                alignment="center"
            ),
            style={
                "width":"100%", 
                "height":"100%"
            }
        )


    def callbacks(self):
        @callback(
            Output(f"temp-card-{self.sensor_id}-{self.field}-{self.stat_method}", "children"),
            Input("temp-dropdown", "value")
        )
        def update_stat(temp_u):
            df = self.test_df
            try:
                df = df.copy()
                if temp_u == "f":
                    df = df[df["sensor_id" == self.sensor_id]]
                    df[self.field] = df[self.field].apply(c_to_f)
                stat_value = self.calculate_stat(df)
                formatted_stat =  f"{stat_value:.2f} {temp_u}°" 
                return self._layout(formatted_stat)
            except Exception:
                return self._layout(f"Error calculating {self.stat_method} for {self.field}")



