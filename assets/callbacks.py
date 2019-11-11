from server import app
from dash.dependencies import Output, Input
import pages.employees as emp
import pages.programs as pgm
import pages.home as home


# These callbacks handle main page functionality like content loading
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/employees':
        return emp.Employees()
    if pathname == '/programs':
        return pgm.Programs()
    if pathname == '/':
        return home.Home()
    if pathname == '/':
        return Login(app)


# These callbacks just set the active class for the navbar so it colors
# properly
@app.callback(
    Output('homeLink', 'className'),
    [Input('url', 'pathname')])
def HomeLink(pathname):
    if pathname == '/':
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
