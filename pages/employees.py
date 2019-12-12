# Dash
import dash_html_components as html
import dash_table as dt

# Local assets import
import assets.SQL as sql
import assets.models as models

employees = sql.get_rows(models.EmployeeData)


def employee_page_layout():
    layout = dt.DataTable(
        style_data={
            'whitespace': 'normal',
            'height': 'auto',
            'overflow': 'hidden',
            'textOverflow': 'ellipses',
            'maxWidth': 0
        },
        id='Employees',
        columns=[{'name': i, 'id': i} for i in dir(models.EmployeeData) if not i.startswith('_')],
        data=[{'name_first': i.name_first,
               'name_last': i.name_last,
               'function': i.function,
               'functions': i.functions,
               'job_code': i.job_code,
               'programs': i.programs,
               'date_start': i.date_start} for i in employees],
        editable=False,
        filter_action='custom',
        sort_action='native',
        sort_mode='single',
        row_deletable=False,
        hidden_columns=[
            'id',
            'metadata',
            'is_admin',
            'level',
            'number',
            'employee_number',
            'assigned_function',
            'assigned_programs',
            'job_title',
            'date_end'],
        style_as_list_view=True,
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        row_selectable='single'
    ),
    html.Div(id='employee-container')
    return layout


# For debugging
# for (key, value) in count.items():
#     print(key, '::', value)
#     total += value
# print('{0} total staff'.format(total))
