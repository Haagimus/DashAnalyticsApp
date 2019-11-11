import dash_html_components as html


def Home():
    content = html.Div([
        html.Img(src='./assets/Images/cat_peel.jpg', className='center')
    ])
    return content
