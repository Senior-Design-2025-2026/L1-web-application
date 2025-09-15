from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Union, List, Dict

from typing import Optional


def flex_builder(
    direction: str = "row",
    children: List[html.Div] = None,
    bordered: bool = False,
    size: str = "md",
    justification: Optional[str] = None,
    alignment: Optional[str] = None,
    fill: bool = True
) -> html.Div:
    """
    Creates a styled Dash container (Div) with configurable direction, size, justification, alignment, and child elements.

    Args:
        direction (str): Flex direction, either 'row' or 'col'.
        children (List[html.Div]): List of Dash HTML Div children to include in the container.
        size (str): Size keyword for both padding and gap (e.g., 'xl', 'lg', 'md', 'sm', 'xs').
        bordered (bool): If True, container contains a light border. Defaults to False (no border).
        justification (str, optional): Flexbox justification (e.g., 'flex-start', 'center', 'flex-end', 'space-between', 'space-around', 'space-evenly').
            Controls alignment along the main axis (the direction of the flex: 'row' = horizontal, 'col' = vertical). Defaults to None.
        alignment (str, optional): Flexbox alignment (e.g., 'stretch', 'center', 'flex-start', 'flex-end', 'baseline').
            Controls alignment along the cross axis (perpendicular to the flex direction: 'row' = vertical, 'col' = horizontal). Defaults to None.
        fill (bool): fully stretch along main axis

    Returns:
        html.Div: A Dash HTML Div styled as a flex container with the specified properties.

    Raises:
        ValueError: If direction or size is not valid.
    """
    if direction not in ["row", "column"]:
        raise ValueError("invalid direction; available directions are ['row', 'col']")

    size_map = {
        "xlarge": 24,
        "xl": 24,
        "large": 20,
        "lg": 20,
        "medium": 16,
        "md": 16,
        "small": 12,
        "sm": 12,
        "xsmall": 8,
        "xs": 8
    }
    if size not in size_map:
        raise ValueError("invalid size; available sizes are ['xl', 'lg', 'md', 'sm', 'xs']")

    padding_px = size_map[size]
    gap_px = padding_px // 2

    border = "1px solid #C7C6C5" if bordered else None

    style = {
        "display": "flex",
        "flex-direction": direction,
        "gap": f"{gap_px}px",
        "padding": f"{padding_px}px",
        "border": border,
        "border-radius": "4px"
    }
    if justification:
        style["justify-content"] = justification
    if alignment:
        style["align-items"] = alignment
    if direction == "row" and fill:
        style["width"] = "100%"
    if direction == "col" and fill:
        style["height"] = "100%"

    return html.Div(
        children,
        style=style
    )

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
        searchable=False,
        persistence=True,
        persistence_type="session",
        style={
            "color": "#666666",
            "font-weight": "normal",
            "width": "100%"
        }
    )

    return html.Div(
        flex_builder(
            direction="column",
            alignment="start",
            children=[
                _label,
                _dropdown
            ]
        ), 
        style={
            "width":"100%"
            }
        )

def textbox_builder(label: str, id: str, value: str = "", placeholder: str = "") -> html.Div:
    """
    Creates a styled Dash textbox (input) component with a label.

    Args:
        label (str): The text to display above the textbox.
        id (str): The unique identifier for the textbox component.
        value (str, optional): The default value for the textbox.
        placeholder (str, optional): Placeholder text for the textbox.

    Returns:
        html.Div: A Dash HTML Div containing the label and textbox, styled in a column layout.
    """
    _label = html.Div(
        label + ":",
        style={
            "color": "#454545",
            "font-weight": "normal"
        }
    )

    _textbox = dcc.Input(
        id=id,
        value=value,
        placeholder=placeholder,
        type="text",
        style={
            "color": "#666666",
            "font-weight": "normal",
            "width": "100%"
        }
    )

    return html.Div(
        flex_builder(
            direction="column",
            alignment="start",
            children=[
                _label,
                _textbox
            ]
        ), 
        style={
            "width":"100%"
            }
        )

def toasty_button(id: str, label: Union[str, html.Div], color: str = "secondary", toast_message: Union[str, html.Div] = "empty message :(", duration_ms: int = 3000, position: str = "top", disabled: bool = False):
    """
    Creates a button that triggers a toast notification.

    Args:
        id (str): Unique identifier for the button and toast.
        label (Union[str, html.Div]): Label for the button. Can be a string or an HTML Div.
        color (str): Color of the button. Defaults to "secondary".
        toast_message (str): Message displayed in the toast. Defaults to "empty message :(".
        duration_ms (int): Duration the toast is visible in milliseconds. Defaults to 3000.
        position (str): Position of the toast. Defaults to "top".
        disabled (bool): ability of the button to recognize a click.

    Returns:
        html.Div: A Div containing the button and toast components.
    """
    btn_id = id
    toast_id = id + "-toast"

    print(toast_id)
    btn = html.Div([
        dbc.Button(
            label,
            id=btn_id,
            color=color,
            n_clicks=0,
            outline=True,
            disabled=disabled
        ),
        dbc.Toast(
            toast_message,
            id=toast_id,
            header=html.Div(f"{id}", style={"font-weight":"bold"}),
            icon="success",
            is_open=False,
            duration=duration_ms,
            style={
                "position": "fixed",
                "top": 66, 
                "right": 10, 
                "width": 350
            },
        )
    ])

    return btn