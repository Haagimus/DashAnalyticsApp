import dash_html_components as html

from app import app
from utils import DashRouter, DashNavBar
from pages import employees, programs
from components import fa


# Ordered iterable of routes: tuples of (route, layout), where 'route' is a
# string corresponding to path of the route (will be prefixed with Dash's
# 'routes_pathname_prefix' and 'layout' is a Dash Component.
urls = (
    ("", character_counter.get_layout),
    ("employees", employees.layout),
    ("programs", programs.layout),
)

# Ordered iterable of navbar items: tuples of `(route, display)`, where `route`
# is a string corresponding to path of the route (will be prefixed with
# 'routes_pathname_prefix') and 'display' is a valid value for the `children`
# keyword argument for a Dash component (ie a Dash Component or a string).
nav_items = (
    ("employees", html.Div([fa("fas fa-chart-area"), "Employees"])),
    ("programs", html.Div([fa("fas fa-chart-line"), "Programs"])),
)

router = DashRouter(app, urls)
navbar = DashNavBar(app, nav_items)
