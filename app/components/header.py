import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Output, Input, callback, html, get_asset_url
import dash_bootstrap_components as dbc
from components.theme_toggle import theme_toggle
from dash import Dash, Input, Output,  clientside_callback

LOGO_DARK = "iowa-gold.png"
LOGO_LIGHT = "iowa-black.png"

PAGE_LINKS= {
    "Home": "mdi:home-outline",    
    "Analytics": "raphael:temp",
    "Configuration": "material-symbols:mail-outline",
}

LINKEDIN_ICON = "mdi:linkedin"
LINKEDIN_LINKS = {
    "Matt Krueger": "https://www.linkedin.com/in/mattnkrueger/",
    "Sage Marks": "https://www.linkedin.com/in/sage-marks/",
    "Steven Austin": "https://wwww.linkedin.com/in/steven-austin-does-not-have-a-linked-in",
    "Zack Mulholland": "https://www.linkedin.com/in/zack-mulholland-317914254/",
}

PDF_ICON = "uiw:file-pdf"
GITHUB_ICON = "mdi:github"
DOCUMENTATION_LINKS = {
    "Project Requirements": "https://github.com/Senior-Design-2025-2026/L1-web-server/blob/main/lab-1.pdf",
    "Senior Design Team 3": "https://github.com/Senior-Design-2025-2026",
    "Server Code": "https://github.com/Senior-Design-2025-2026/L1-web-server",
    "Embedded Code": "https://github.com/Senior-Design-2025-2026/L1-embedded-thermostat",
}

# ----- build menu items ---- #
# 1. Page links
page_items = []

for key,val in PAGE_LINKS.items():
    href = f"/{key.lower()}"
    page_items.append(
        dmc.NavLink(
            label=dmc.Text(
                key, 
                fz={"base":14, "sm":10, "md":12, "lg":18}
            ),
            href=href,
            leftSection=DashIconify(icon=val),
        )
    )

# 2. Linked In links
nested_linkedIn_items = []

for key,val in LINKEDIN_LINKS.items():
    nested_linkedIn_items.append(
        dmc.MenuItem(
            key,
            href=val,
            target="_blank",
            leftSection=DashIconify(
                icon=LINKEDIN_ICON,
                color="0077B5"
            ),
            fz={"base":14, "sm":10, "md":14, "lg":18}
        )
    )

linkedIn_submenu = dmc.SubMenu([
    dmc.SubMenuTarget(
        dmc.SubMenuItem(
            "Team 3 Members",
            fz={"base":14, "sm":10, "md":14, "lg":18}
        )
    ),
    dmc.SubMenuDropdown(
        nested_linkedIn_items,
    )
])

# 3. Documetation links
nested_documentation_items = []

for key,val in DOCUMENTATION_LINKS.items():
    if "pdf" in val:
        icon = PDF_ICON
        color = "#F40F02"
    elif "github" in val:
        icon = GITHUB_ICON
        color = "#211F1F"

    nested_documentation_items.append(
        dmc.MenuItem(
            key,
            href=val,
            target="_blank",
            leftSection=DashIconify(
                icon=icon,
                color=color
            ),
            fz={"base":14, "sm":10, "md":14, "lg":18}
        )
    )

documentation_submenu = dmc.SubMenu([
    dmc.SubMenuTarget(
        dmc.SubMenuItem(
            "Project Docs",
            fz={"base":14, "sm":10, "md":14, "lg":18}
        )
    ),
    dmc.SubMenuDropdown(
        nested_documentation_items
    )
])

# --------------------- HEADER --------------------- #

def header():
    lhs = dmc.Group(
        [
            dmc.Image(
                id="header-logo",
                w="90",
                h="45",
                fit="fit"
            ),
            html.Div(
                id="header-divider",
                style={
                        "background-color": "#c7c6c5",
                        "border-radius": "20px",
                        "width": "1px",
                        "height": "50%"
                }
            ),
            dmc.Title(
                "Herky's Nest",
                id="header-title",
                size="xl"
            )
        ],
        h="100%",
        px="md"
    )

    menu = dmc.Menu(
        [
            dmc.MenuTarget(
                dmc.ActionIcon(
                    DashIconify(
                        icon="stash:burger-classic-light"
                    ),
                    size="lg",
                    color=dmc.DEFAULT_THEME["colors"]["yellow"][6]
                ),
            ),
            dmc.MenuDropdown(
                [
                    dmc.MenuLabel(
                        "Pages",
                        fz="md"
                    ),
                    *page_items,
                    dmc.MenuDivider(),
                    dmc.MenuLabel(
                        "External Links",
                        fz="md"
                    ),
                    documentation_submenu,
                    linkedIn_submenu
                ]
            )
        ]
    )

    rhs = dmc.Center(
        [
            html.Div(
                theme_toggle, 
                style={
                    "marginRight":"1em"
                }
                ),
            menu
        ],
        h="100%",
    )

    return dmc.Group(
            [
                lhs,
                rhs
            ],
            h="100%",
            align="center",
            justify="space-between",
            px="sm"
        )

@callback(
    Output("header-logo", "src"),
    Output("header-title", "c"),
    Input("color-scheme-switch", "checked")
)
def header_theme_toggle(checked):
    if checked:  
        return get_asset_url(LOGO_DARK), "white"
    else:
        return get_asset_url(LOGO_LIGHT), dmc.DEFAULT_THEME["colors"]["yellow"][6]