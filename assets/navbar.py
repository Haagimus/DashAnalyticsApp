import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# When new pages are added, update list with href to location
def Navbar():
    navbar = html.Ul([
        html.Li([dcc.Link('Home', id='homeLink', href='/')]),
        html.Li([dcc.Link('Employee', id='empLink', href='/employees')]),
        html.Li([dcc.Link('Programs', id='pgmLink', href='/programs')])
    ])

    return navbar
