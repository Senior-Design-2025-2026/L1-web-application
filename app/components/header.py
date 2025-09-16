import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Output, Input, callback, html, get_asset_url
import dash_bootstrap_components as dbc
from components.theme_toggle import theme_toggle
from dash import Dash, Input, Output,  clientside_callback

LOGO_DARK = get_asset_url("iowa-gold.png")
LOGO_LIGHT = get_asset_url("iowa-black.png")

PAGE_LINKS= {
    "Home": "mdi:home-outline",         # vals are icons
    "Dashboard": "raphael:temp",
    "Config": "material-symbols:mail-outline",
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
    "Team Github": "https://github.com/Senior-Design-2025-2026",
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
            label=key,
            href=href,
            leftSection=DashIconify(icon=val)
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
            leftSection=DashIconify(icon=LINKEDIN_ICON)
        )
    )

linkedIn_submenu = dmc.SubMenu([
    dmc.SubMenuTarget(
        dmc.SubMenuItem(
            "Team Members"
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
            leftSection=DashIconify(icon=icon)
        )
    )

documentation_submenu = dmc.SubMenu([
    dmc.SubMenuTarget(
        dmc.SubMenuItem(
            "Project Docs"
        )
    ),
    dmc.SubMenuDropdown(
        nested_documentation_items
    )
])

def header():
    title = "ECE Senior Design Lab 1 - Team 3"

    # lhs
    lhs = dmc.Group(
        [
            dmc.Image(
                id="header-logo",
                src=LOGO_DARK,
                w=80
            ),
            dmc.Divider(
                orientation="vertical",
                size="xs",
                color="gray",
            ),
            dmc.Text(
                title,
                c="white",
                fw=700,
                size="xl",
                id="header-title"
            ),
        ],
        gap="md",
        align="center",
    )

    # rhs
    rhs = dmc.Group(
        [
            theme_toggle,
            dmc.Menu(
                [
                    dmc.MenuTarget(
                        dmc.ActionIcon(
                            DashIconify(icon="stash:burger-classic-light", width=20),
                            w=40,
                            h=40,
                            color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
                            variant="filled",    
                            radius="md"
                        )
                    ),
                    dmc.MenuDropdown(
                        [
                            dmc.MenuLabel("Pages"),
                            *page_items,
                            dmc.MenuDivider(),
                            dmc.MenuLabel("External Links"),
                            linkedIn_submenu,
                            documentation_submenu,
                        ]
                    ),
                ]
            ),
        ],
        align="center",
    )

    # main header bar
    return dmc.Flex(
        [lhs, rhs],
        justify="space-between",
        align="center",
        style={"width": "100%", "padding": "8px 20px"}
    )

@callback(
    Output("header-logo", "src"),
    Output("header-title", "c"),
    Input("color-scheme-switch", "checked")
)
def color_header(checked):
    if checked:                 # checked is dark mode
        return LOGO_DARK, "white"
    else:
        return LOGO_LIGHT, "#FFDD00"