import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash_table as dt

pd.read_excel(".\assets\Sector_DevOps_Status_FX.xls")

programs_layout = html.Div([
    html.H2('Under Construction'),
    html.Div(id='programs-content')
    ])

