from server import app
from dash.dependencies import Output, Input
from dash import dependencies
from dash.development.base_component import Component
import pages.employees as emp
import pages.programs as pgm
import pages.home as home
import pages.capacity as cap
import pages.login as log


# These callbacks handle main page functionality like content loading
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/employees':
        return emp.Employees()
    if pathname == '/programs':
        return pgm.Programs()
    if pathname == '/capacity':
        return cap.Capacity()
    if pathname == '/home':
        return home.Home()
    if pathname == '/':
        return log.Login()


# These callbacks just set the active class for the navbar so it colors
# properly
@app.callback(
    Output('homeLink', 'className'),
    [Input('url', 'pathname')])
def HomeLink(pathname):
    if pathname == '/home':
        return 'active'


@app.callback(
    Output('empLink', 'className'),
    [Input('url', 'pathname')])
def EmpLink(pathname):
    if pathname == '/employees':
        return 'active'


@app.callback(
    Output('pgmLink', 'className'),
    [Input('url', 'pathname')])
def PgmLink(pathname):
    if pathname == '/programs':
        return 'active'


@app.callback(
    Output('capLink', 'className'),
    [Input('url', 'pathname')])
def CapLink(pathname):
    if pathname == '/capacity':
        return 'active'

# class Output(dependencies.Output):
#     """Output of a callback."""
#     def __init__(self,component: Component)
