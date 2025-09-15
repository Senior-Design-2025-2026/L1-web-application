from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd

 
def plot_sensor_trace(fig: go.Figure, df: pd.DataFrame, id: int, line: dict):
    sensor_df = df[df["id"] == 1]
    fig.add_trace(
        go.Scatter(
            x=sensor_df["time"],
            y=sensor_df["temperature"],
            mode="lines",
            name=f"Sensor {id}",
            line=line
        )
    )
    
def create_chart(
        df: pd.DataFrame,
        temp_unit: str = "c",       # default per embedded side
        time_unit: str = "s",       # default per this server
) -> go.Figure:
    """
    Plots a line chart of temperature readings for two sensors.

    Args:
        df (pd.DataFrame): DataFrame containing columns ['sensor_id', 'time', 'temp'].
        temp_unit (str): y axis with temp unit
        time_unit (str): x axis with time unit

    Returns:
        go.Figure: Plotly figure object for the temperature readings.
    """
    # TODO REMOVE
    df = pd.DataFrame({
        "id": [1]*10 + [2]*10,
        "time": list(range(10)) + list(range(10)),
        "temperature": [20 + i for i in range(10)] + [18 + i*3 for i in range(10)]
    })

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
        xaxis_title=f"Time ({time_unit})",
        yaxis_title=f"Temperature ({temp_unit})",
        legend_title="Sensor",
        template="simple_white"
    )

    return html.Div(
        dcc.Graph(figure=fig)
    )