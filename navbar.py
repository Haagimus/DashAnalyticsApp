# this file will create the navabar for the top of pages
import dash_core_components as dcc
import dash_html_components as html


def Navbar():
    navbar = html.Ul([
        html.Li([dcc.Link('Home', href='/')]),
        html.Li([dcc.Link('Employee', href='/employees.py')]),
        html.Li([dcc.Link('Programs', href='/')])
    ])

    return navbar
