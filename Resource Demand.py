import dash
import dash_html_components as html

import employees

empTable = employees.EmployeeTable()

app = dash.Dash(__name__)

app.layout = html.Div([
    empTable
])

if __name__ == '__main__':
    app.run_server(debug=False)
