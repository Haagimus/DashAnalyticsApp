# -*- coding: utf-8 -*-
# This file is the main landing page for the application
import dash
import dash_core_components as dcc
import dash_html_components as html

import navbar

app = dash.Dash(__name__)
nav = navbar.Navbar()

app.layout = html.Div([
    # represents the URL bar, doesn't render anythin
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    return html.Div([
        nav,
        html.H3('You are on page {}'.format(pathname))
    ])


if __name__ == '__main__':
    app.run_server(debug=False)
