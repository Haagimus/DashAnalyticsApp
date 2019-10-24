import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html

import employees

app = dash.Dash(__name__)

app.layout = html.Div([
    dt.DataTable(
        style_data={
            'whitespace': 'normal',
            'height': 'auto',
            'overflow': 'hidden',
            'textOverflow': 'ellipses',
            'maxWidth': 0,
        },
        id='Employees',
        columns=[
            {'name': i, 'id': i, 'selectable': True} for i in employees.empDF.columns
        ],
        data=employees.empDF.to_dict('records'),
        editable=True,
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        row_deletable=False,
        hidden_columns=['Long_Text', 'Name_Full'],
    ),
    html.Div(id='employee-container')
])

if __name__ == '__main__':
    app.run_server(debug=False)
