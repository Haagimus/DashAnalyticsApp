import dash_html_components as html
import pandas as pd
import dash_table as dt


# df_excel = pd.read_excel("./assets/Files/Sector_DevOps_Status_FX.xlsx")
#
#
# def make_dash_table(df):
#     table = []
#     table.append(html.Tr([html.Th(col) for col in df.columns], style={
#                  'background-color': 'darkgrey'}))
#     for index, row in df.iterrows():
#         html_row = []
#         for i in range(len(row)):
#             if pd.isna(row[0]) and pd.isna(row[1]):
#                 continue
#             else:
#                 str = row[i]
#                 fmt = color_cells(str)
#                 html_row.append(
#                     html.Td([row[i]], style={'background-color': fmt}))
#         table.append(html.Tr(html_row))
#     return table
#
#
# def color_cells(str):
#     fmt = {'No': 'darkred', 'Yes': 'darkgreen',
#            'Continue': 'darkgreen', 'Planned': 'darkorange'}
#     if str not in fmt:
#         fmt.setdefault(str, 'darkgrey')
#     return fmt[str]


def program_page_layout():
    layout = html.Div(id='work-in-progress')
    return layout
