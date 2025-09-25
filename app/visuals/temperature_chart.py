from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd

 
def plot_sensor_trace(fig: go.Figure, df: pd.DataFrame, id: int, line: dict):
    sensor_df = df[df["id"] == 1]
    fig.add_trace(
        go.Scatter(
            x=sensor_df["time"],
            y=sensor_df["temperatureSensor" + str(id) + "Data"],
            mode="lines",
            name=f"Sensor {id}",
            line=line
        )
    )
    
def create_chart(
        df: pd.DataFrame,
        temp_unit: str = "C",       # default per embedded side
        time_unit: str = "s",       # default per this server
) -> html.Div:
    """
    Plots a line chart of temperature readings for two sensors.

    Args:
        df (pd.DataFrame): DataFrame containing columns ['sensor_id', 'time', 'temp'].
        temp_unit (str): y axis with temp unit
        time_unit (str): x axis with time unit

    Returns:
        go.Figure: Plotly figure object for the temperature readings.
    """

    line_width = 2

    line_s1 = {
        "color": "#666666",
        "width": line_width,
        "dash": "solid"
    }

    line_s2 = {
        "color": "#454545",
        "width": line_width,
        "dash": "dash"
    }

    fig = go.Figure()
    plot_sensor_trace(fig, df, 1, line_s1)
    plot_sensor_trace(fig, df, 2, line_s2)

    fig.update_layout(
        xaxis_title=f"Seconds Ago ({time_unit})",
        yaxis_title=f"Temperature ({temp_unit})",
        yaxis=dict(range=[10, 50] if temp_unit == 'C' else [50, 122]),
        xaxis=dict(autorange="reversed"),
        legend_title="Sensor",
        template="simple_white"
    )

    return html.Div(
        dcc.Graph(figure=fig)
    )