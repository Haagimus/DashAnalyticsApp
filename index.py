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
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/employees':
        return EmployeeTable()
    if pathname == '/programs':
        return Programs()
    if pathname == '/':
        return html.Img(src='./assets/Images/dog.jpg', className ='center')

# These callbacks just set the active class for the navbar so it colors properly
@app.callback(Output('homeLink', 'className'), [Input('url', 'pathname')])
def HomeLink(pathname):
    if pathname == '/':
        return 'active'


@app.callback(Output('empLink', 'className'), [Input('url', 'pathname')])
def EmpLink(pathname):
    if pathname == '/employees':
        return 'active'


@app.callback(Output('pgmLink', 'className'), [Input('url', 'pathname')])
def PgmLink(pathname):
    if pathname == '/programs':
        return 'active'


if __name__ == '__main__':
    # Uncomment this line to run the actual server
    #app.run_server(debug=False, host='166.20.109.188', port='8080')
    
    # Uncomment this line to debug locally
    app.run_server(debug=True, host='127.0.0.1', port='8080')
