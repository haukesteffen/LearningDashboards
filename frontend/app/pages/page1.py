import requests
from dash import Dash, register_page, Output, Input, html, dcc

register_page(__name__, path='/', name='Page 1')

layout = html.Div([
    dcc.Input(
        id="input",
        placeholder="input comment id"
    ),
    html.Div(id='textarea')
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