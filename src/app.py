import requests
import plotly.express as px
import pandas as pd
from dash import Dash, html, dash_table, dcc, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.LUX])
load_figure_template('LUX')


# App layout
app.layout = html.Div([
    html.Div(
        children='Hacker News Popularity by Year'
    ),
    html.Div([
        dcc.Input(value="Kubernetes", id="input", type="text", placeholder="Kubernetes", debounce=True),
    ]),
    html.Div(
        dash_table.DataTable(
            id='data-table',
            page_size=15,
            style_cell={
                'textOverflow': 'ellipsis',
                'maxWidth': 0
            },
            export_format='csv',
        )
    ),
    html.Div(
        dcc.Graph(
            id='popularity-over-time-graph'
        )
    )
    ])

# Add controls to build the interaction
@app.callback(
    Output('data-table', 'data'),
    Input('input', 'value'),
)
def display_user_data(string: str):
    if string:
        response = requests.get(f"http://localhost:8000/popularity/?string={string}")
        if response.status_code == 200:
            popularity_data = response.json()
            return popularity_data
    return []

@app.callback(
    Output('popularity-over-time-graph', 'figure'),
    Input('data-table', 'data'),
)
def update_graph(data):
    if data:
        df = pd.DataFrame(data).rename(columns={0: 'Year', 1: 'Number of Mentions'})
        fig = px.scatter(df, x='Year', y='Number of Mentions')
        return fig
    return {}

# Run the app
if __name__ == '__main__':
    app.run()
