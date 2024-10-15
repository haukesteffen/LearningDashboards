import requests
from dash import Dash, register_page, Output, Input, html, dcc
import dash_bootstrap_components as dbc

register_page(__name__, path='/page1', name='Page 1')

layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1(children='Comment Viewer'),
            width=12
        ),
        justify='center'
    ),
    dbc.Row([
        dbc.Row(
            dbc.Col([
                html.Label('Input Comment ID:'),
                dcc.Input(
                    id='input',
                    placeholder='Input comment ID',
                    type='number',
                ),
            ]),
            justify='center',
            className='single-dropdown-container'
        ),
    ], className='multiple-dropdown-container'),
    dbc.Row(
        dbc.Col(
            html.Div(id='textarea'),
            className='graph-container'
        ),
        justify='center'
    )
])

def register_callbacks(app: Dash):
    @app.callback(
        Output('textarea', 'children'),
        Input('input', 'value')
    )
    def display_comment(comment_id: int):
        if comment_id:
            response = requests.get(f"http://localhost:8000/comment/?comment_id={comment_id}")
            if response.status_code == 200:
                comment = response.json()['text']
                return comment
        return []
