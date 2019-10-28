# -*- coding: utf-8 -*-
# This file is the main landing page for the application
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages.employees import EmployeeTable
from pages.programs import Programs
from assets.navbar import Navbar

app = dash.Dash(__name__)
nav = Navbar()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content')
])


# Index Page Callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/employees':
        return EmployeeTable()
    if pathname == '/programs':
        return Programs()


if __name__ == '__main__':
    app.run_server(debug=True)
