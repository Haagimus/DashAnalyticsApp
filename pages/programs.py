import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash_table as dt

df_excel = pd.read_excel("./assets/Files/Sector_DevOps_Status_FX.xlsx")

def make_dash_table(df):
    table = []
    table.append(html.Tr([html.Th(col) for col in df.columns], style={'background-color': 'darkgrey'})) 
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            if pd.isna(row[0]) and pd.isna(row[1]):
               continue
            else:
               str = row[i]
               fmt=color_cells(str)
               html_row.append(html.Td([row[i]], style={'background-color': fmt}))
        table.append(html.Tr(html_row))
    return table

def color_cells(str):
    fmt = { 'No': 'darkred', 'Yes': 'darkgreen', 'Continue': 'darkgreen', 'Planned': 'darkorange'}
    if str not in fmt:
        fmt.setdefault(str, 'darkgrey')
    return fmt[str] 

def Programs():
    content = html.Div([
        html.H2('Under Construction'),
        html.Div(id='programs-content'),
        html.Table(make_dash_table(df_excel))
                   ])
    return content