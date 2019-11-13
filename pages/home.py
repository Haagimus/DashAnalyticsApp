import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from server import app


def Home():
    content = html.Div([
        html.Img(src='./assets/Images/cat_peel.jpg', className='center'),
    ])
    return content
