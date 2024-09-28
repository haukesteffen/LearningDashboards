import os
import requests
import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from sqlalchemy import create_engine


# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.LUX])
load_figure_template('LUX')


# App layout
app.layout = html.Div([
    html.Div(
        children='My First App with Dynamic Data'
    ),
    dcc.Input(id="comment-input", type="text", placeholder="Input Comment ID"),
    dash_table.DataTable(
        id='comment-table',
        page_size=10,
        style_cell={
            'textOverflow': 'ellipsis',
            'maxWidth': 0
        })
    ])

# Add controls to build the interaction
@app.callback(
    Output('comment-table', 'data'),
    Input('comment-input', 'value')
)
def display_user_data(comment_id):
    if comment_id:
        # Fetch the selected user's data from FastAPI
        response = requests.get(f"http://localhost:8000/comment/{comment_id}")
        if response.status_code == 200:
            comment_data = response.json()
            return [comment_data]
    return []

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
