# -*- coding: utf-8 -*-
# This file is the main landing page for the application
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Ul([
        html.Li([html.A(['Home'])]),
        html.Li([html.A(['Page 2'])]),
        html.Li([html.A(['Page 3'])])
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
