import dash_html_components as html
import dash_core_components as dcc


def Navbar():
    navbar = html.Ul([
        html.Li([dcc.Link('Home', href='/')]),
        html.Li([dcc.Link('Employee', href='/employees')]),
        html.Li([dcc.Link('Programs', href='/programs')])
    ])

    return navbar
