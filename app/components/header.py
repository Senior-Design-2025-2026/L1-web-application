import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Output, Input, callback, html, get_asset_url
import dash_bootstrap_components as dbc
from components.theme_toggle import theme_toggle

LOGO_DARK = "/app/assets/iowa-gold.png"
LOGO_LIGHT = "/app/assets/iowa-black.png"

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

# ---------- HEADER COMPONENT ---------- # 
def header():
    logo = get_asset_url(LOGO_DARK)
    title = "ECE Senior Design Lab 1 (Team 3)"

    lhs = html.Div(
        [
            html.Img(
                src=logo,
            ),
            html.Div(
                title,
                style={
                    "font-size":"24px",
                    "font-weight":"bold",
                    "color":"#FFDD00"
                }
            )
        ],
        style={
            "display":"flex",
            "justify-contents":"space-between",
            "align-items":"center",
        }
    )

    rhs = dmc.Menu(
        [
            theme_toggle,
            dmc.MenuTarget(
                dmc.ActionIcon(DashIconify(icon="stash:burger-classic-light"))
            ),

            dmc.MenuDropdown(
                [
                    # pages
                    dmc.MenuLabel("Pages"),
                    *page_items,

                    # divider
                    dmc.MenuDivider(),
                    dmc.MenuLabel("External Links"),

                    # linked in
                    linkedIn_submenu,

                    # docs
                    documentation_submenu
                ]
            )
        ],
    )

    header = html.Div(
        [
            lhs,
            rhs,
        ],
        style={
            "display":"flex",
            "justify-contents":"space-between",
            "align-items":"center",
            "width":"100%"
        }
    )

    return header