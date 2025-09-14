
from dash import html, dcc, callback, Output, Input
from typing import Optional, Union, List, Dict

def dropdown_builder(label: str, id: str, options: List[Dict], clearable: Union[bool, None] = False, value: Union[str, list, None] = None) -> html.Div:
    """
    Creates a styled Dash dropdown component with a label.

    Args:
        label (str): The text to display above the dropdown.
        id (str): The unique identifier for the dropdown component.
        options (List[Dict]): A list of option dictionaries for the dropdown. Each dict should have 'label' and 'value' keys.
        clearable (bool | None, optional): if True, the dropdown may be cleared. If None, defaults to False (not clearable).
        value (str | list | None, optional): The default selected value(s). If None, defaults to the first option's value.

    Returns:
        html.Div: A Dash HTML Div containing the label and dropdown, styled in a column layout.
    """
    _label = html.Div(
        label + ":",
        style={
            "color": "#454545",
            "font-weight": "normal"
        }
    )

    _dropdown = dcc.Dropdown(
        id=id,
        options=options,
        value=value if value is not None else options[0].get("value") if options else None,
        clearable=clearable,
        style={
            "color": "#666666",
            "font-weight": "normal"
        }
    )

    return html.Div([
        _label,
        _dropdown,
    ],
    style={
        "display": "flex",
        "flex-direction": "column",
        "gap": "4px",
        "width": "100%"
    })