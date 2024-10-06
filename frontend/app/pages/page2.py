# page2.py

import requests
from dash import Dash, register_page, Output, Input, State, html, dcc, callback
import plotly.express as px
import pandas as pd

register_page(__name__, path='/page2', name='Page 2')

layout = html.Div([
    html.H1('Term Popularity Over Time'),
    dcc.Store(id='terms_store'),
    html.Div([
        html.Label('Select Term:'),
        dcc.Dropdown(
            id='term_dropdown',
            options=[], 
            placeholder='Select a term',
            style={'width': '300px', 'marginRight': '10px'}
        ),
        html.Label('Select Aggregation Type:'),
        dcc.Dropdown(
            id='agg_dropdown',
            options=[
                {'label': 'Year', 'value': 'year'},
                {'label': 'Month', 'value': 'month'},
                {'label': 'Week', 'value': 'week'}
            ],
            value='year',
            clearable=False,
            style={'width': '150px'}
        ),
    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '20px'}),
    dcc.Graph(id='term_popularity_graph'),
])

def register_callbacks(app: Dash):
    @app.callback(
        [Output('term_dropdown', 'options'),
         Output('terms_store', 'data')],
        Input('term_dropdown', 'id')
    )
    def load_terms(_):
        response = requests.get('http://localhost:8000/termpop/terms')
        if response.status_code == 200:
            terms = response.json()
            if 'id' in terms[0]:
                options = [{'label': term['term'], 'value': term['id']} for term in terms]
            else:
                return [], []
            return options, terms
        else:
            return [], []

    @app.callback(
        Output('term_popularity_graph', 'figure'),
        Input('term_dropdown', 'value'),
        Input('agg_dropdown', 'value'),
        State('terms_store', 'data')
    )
    def update_graph(term_id, agg, terms):
        if term_id is not None and agg is not None:
            response = requests.get(f'http://localhost:8000/termpop/agg?term_id={term_id}&agg={agg}')
            if response.status_code == 200:
                data = response.json()
                if data:
                    df = pd.DataFrame(data)
                    if agg == 'year':
                        df['time'] = df['year'].astype(str)
                    elif agg == 'month':
                        df['time'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
                    elif agg == 'week':
                        df['time'] = df['year'].astype(str) + '-W' + df['week'].astype(str).str.zfill(2)
                    else:
                        df['time'] = df['year'].astype(str)
                    df = df.sort_values('time')
                    term_name = next((term['term'] for term in terms if term['id'] == term_id), 'Selected Term')
                    fig = px.line(df, x='time', y='occurrence_count', title=f'Term Popularity Over Time for "{term_name}"')
                    fig.update_layout(
                        xaxis_title='Time',
                        yaxis_title='Occurrence Count',
                        xaxis_tickangle=-45
                    )
                    return fig
                else:
                    return {
                        'data': [],
                        'layout': {'title': f'No data available for "{term_name}" and aggregation level "{agg}".'}
                    }
            else:
                return {
                    'data': [],
                    'layout': {'title': 'Error fetching data from API.'}
                }
        else:
            return {
                'data': [],
                'layout': {'title': 'Please select a term and an aggregation type.'}
            }
