import dash_core_components as dcc
import dash_html_components as html


card_style = {
    "box-shadow": "0 4px 5px 0 rgba(0,0,0,0.14), 0 1px 10px 0 rgba(0,0,0,0.12), 0 2px 4px -1px rgba(0,0,0,0.3)"
}


def capacity_page_layout():
    # TODO: Add a tab layout to select either the table or the chart
    layout = html.Div([
        dcc.Tabs(
            id='capacity-tabs',
            value='capacity-table',
            children=[
                dcc.Tab(label='Capacity Table',
                        value='capacity-table'),
                dcc.Tab(label='Capacity Chart',
                        value='capacity-chart')
            ],
            colors={
                'border': 'white',
                'primary': 'gold',
                'background': 'cornsilk'
            },
            parent_style=card_style
        ),
        html.Div(
            children=[
                dcc.Loading(id='capacity-tabs-content',
                            type='graph')
            ]
        )]
    )

    return layout
