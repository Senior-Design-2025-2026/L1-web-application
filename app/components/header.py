import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Output, Input, callback, html, get_asset_url
import dash_bootstrap_components as dbc
from components.theme_toggle import theme_toggle
from dash import Dash, Input, Output,  clientside_callback

LOGO_DARK = "iowa-gold.png"
LOGO_LIGHT = "iowa-black.png"

PAGE_LINKS= {
    "Home": "mdi:home-outline",         # vals are icons
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

PDF_ICON = "teenyicons:pdf-outline"
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
            ),
            fz={"base":14, "sm":10, "md":14, "lg":18}
        )
    )

linkedIn_submenu = dmc.SubMenu([
    dmc.SubMenuTarget(
        dmc.SubMenuItem(
            "Team 3",
            fz={"base":14, "sm":10, "md":14, "lg":18}
        )
    ),
    dmc.SubMenuDropdown(
        nested_linkedIn_items
    )
])

# 3. Documetation links
nested_documentation_items = []

for key,val in DOCUMENTATION_LINKS.items():
    if "pdf" in val:
        icon = PDF_ICON
    elif "github" in val:
        icon = GITHUB_ICON

    nested_documentation_items.append(
        dmc.MenuItem(
            key,
            href=val,
            target="_blank",
            leftSection=DashIconify(icon=icon),
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
    title = "ECE Senior Design Lab 1"

    lhs = dmc.Group(
        [
            dmc.Image(
                id="header-logo",
                src=LOGO_DARK,
                w={"base": 40, "sm": 60, "md": 80}, 
            ),
            dmc.Divider(orientation="vertical", size="xs", color="gray"),
            dmc.Text(
                title,
                id="header-title",
                c="white",
                fw=700,
            ),
        ],
        gap={"base": "xs", "sm": "md"},
        align="center",
    )

    rhs = dmc.Group(
        [
            theme_toggle,
            dmc.Menu(
                [
                    dmc.MenuTarget(
                        dmc.ActionIcon(
                            DashIconify(
                                icon="stash:burger-classic-light",
                                width=20
                            ),
                            w={"base": 32, "sm": 36, "md": 40},
                            h={"base": 32, "sm": 36, "md": 40},
                            color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
                            variant="filled",
                            radius="md",
                        )
                    ),
                    dmc.MenuDropdown(
                        [ 
                            dmc.MenuLabel(
                                "Pages", 
                                fz={"base":12, "sm":8, "md":10, "lg":14}
                            ),
                            *page_items,
                            dmc.MenuDivider(),
                            dmc.MenuLabel(
                                "External Links", 
                                fz={"base":12, "sm":8, "md":10, "lg":14}
                            ),
                            linkedIn_submenu, 
                            documentation_submenu, 
                        ]
                    ),
                ]
            ),
        ],
        gap={"base": "xs", "sm": "md"},
        align="center",
    )

    return dmc.Flex(
        [lhs, rhs],
        justify="space-between",
        align="center",
        style={"width": "100%", "padding": "8px 20px"},
    )

@callback(
    Output("header-logo", "src"),
    Output("header-title", "c"),
    Input("color-scheme-switch", "checked")
)
def color_header(checked):
    if checked:                 # checked is dark mode
        return get_asset_url(LOGO_DARK), "white"
    else:
        return get_asset_url(LOGO_LIGHT), dmc.DEFAULT_THEME["colors"]["yellow"][6]