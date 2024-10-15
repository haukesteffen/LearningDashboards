from dash import Dash, register_page, html, dcc
import dash_bootstrap_components as dbc
import dash

register_page(__name__, path='/', name='Homepage')

from . import page1
from . import page2

layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.Div('Welcome to Hacker News Analytics!')
        ),
        justify='center'
    ),
    html.Div(
        [
            html.Div(
                dcc.Link(f"{page['name']}", href=page["relative_path"])
            ) for page in dash.page_registry.values()
        ]
    )
])

def register_callbacks(app: Dash):
    pass 