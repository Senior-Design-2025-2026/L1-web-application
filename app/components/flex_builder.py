from dash import html
from typing import Optional, List


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
