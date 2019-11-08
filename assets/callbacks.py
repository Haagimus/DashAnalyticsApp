from server import app
from pages.employees import empDF, operators, split_filter_part
from dash.dependencies import Output, Input

# Import pages
# from pages.home import Home
# from pages.programs import Programs
# from pages.employees import EmployeeTable


# TODO: Need to figure out how to get this callback working
@app.callback(
    Output('employee-container', "data"),
    [Input('employee-container', "filter_query")])
def update_table(filter):
    filtering_expressions = filter.split(' && ')
    dff = empDF
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.to_dict('records')


# These callbacks handle main page functionality like content loading
# @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/employees':
#         return EmployeeTable()
#     if pathname == '/programs':
#         return Programs()
#     if pathname == '/':
#         return Home()
    # if pathname == '/':
    #     return Login(app)

# These callbacks just set the active class for the navbar so it colors
# properly
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
