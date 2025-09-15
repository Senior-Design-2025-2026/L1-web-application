from dash import html

from components.builders import flex_builder, textbox_builder

class UserConfig:
    def __init__(self, app, config: dict):
        self.config: dict = config
        self.id = self.config.get("id")

        if app is not None:
            self.callbacks()
    
    def render(self) -> html.Div:
        boxes = []

        for val, key in self.config.items():
            if val != "id":
                box = textbox_builder(
                    label=val,
                    id=f"user-{self.id}-{key}",
                    value=key
                )

                boxes.append(box)

        entry = html.Div(
            flex_builder(
                direction="row",
                children=boxes,
                bordered=True,
                justification="start",
                alignment="center"
            ),
            style={
                "width":"100%"
                }
            )

    def callbacks(self):
        ...
        

        
        


