
import requests
from dash import Dash, register_page, Output, Input, html, dcc, callback
import plotly.express as px
import pandas as pd

register_page(__name__, path='/page2', name='Page 2')

layout = html.Div([
    html.H1('Term Popularity Over Time'),
    html.Div([
        html.Label('Enter Term ID:'),
        dcc.Input(
            id='term_id_input',
            type='number',
            value=1,
            min=1,
            placeholder='Enter Term ID',
            style={'marginRight': '10px'}
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
    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}),
    dcc.Graph(id='term_popularity_graph'),
])

def register_callbacks(app: Dash):
    @app.callback(
        Output('term_popularity_graph', 'figure'),
        Input('term_id_input', 'value'),
        Input('agg_dropdown', 'value')
    )
    def update_graph(term_id, agg):
        if term_id is not None and agg is not None:
            # Make API request
            response = requests.get(f'http://localhost:8000/termpop?term_id={term_id}&agg={agg}')
            if response.status_code == 200:
                data = response.json()
                if data:
                    # Convert data to DataFrame
                    df = pd.DataFrame(data)
                    # Create a time variable based on aggregation level
                    if agg == 'year':
                        df['time'] = df['year'].astype(str)
                    elif agg == 'month':
                        df['time'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
                    elif agg == 'week':
                        df['time'] = df['year'].astype(str) + '-W' + df['week'].astype(str).str.zfill(2)
                    else:
                        df['time'] = df['year'].astype(str)
                    # Sort the DataFrame by time
                    df = df.sort_values('time')
                    # Create line plot
                    fig = px.line(df, x='time', y='occurrence_count', title='Term Popularity Over Time')
                    fig.update_layout(
                        xaxis_title='Time',
                        yaxis_title='Occurrence Count',
                        xaxis_tickangle=-45
                    )
                    return fig
                else:
                    return {
                        'data': [],
                        'layout': {'title': 'No data available for the selected term and aggregation level.'}
                    }
            else:
                return {
                    'data': [],
                    'layout': {'title': 'Error fetching data from API.'}
                }
        else:
            return {
                'data': [],
                'layout': {'title': 'Please enter a Term ID and select an aggregation type.'}
            }