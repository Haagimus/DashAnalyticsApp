# -*- coding: utf-8 -*-
# This file is the main landing page for the application
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import employees, programs

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # When new pages are added, update list with href to location
    html.Ul([
        html.Li([dcc.Link('Home', href='/')]),
        html.Li([dcc.Link('Employee', href='/employees')]),
        html.Li([dcc.Link('Programs', href='/programs')])
    ]),
    html.Div(id='page-content')
])


#Index Page Callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/employees':
        return employees.EmployeeTable()
    if pathname == '/programs':
       return programs.programs_layout

if __name__ == '__main__':
    app.run_server(debug=True)
