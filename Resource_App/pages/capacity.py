import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
from pages.employees import function_totals


def Capacity():
    # ft = function_totals()
    content = dt.DataTable(
        # style_data={
        #     'whitespace': 'normal',
        #     'height': 'auto',
        #     'overflow': 'hidden',
        #     'textOverflow': 'ellipses',
        #     'maxWidth': 0
        # },
        # id='Capacity',
        # columns=[{'name': i, 'id': i} for i in ft],
        # editable=False,
        # filter_action='custom',
        # sort_action='native',
        # sort_mode='single',
        # row_deletable=False,
        # style_as_list_view=True,
        # style_header={
        #     'backgroundColor': 'white',
        #     'fontWeight': 'bold'
        # },
        # row_selectable='single'
    ),
    return content
