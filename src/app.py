import os
import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from sqlalchemy import create_engine

# Incorporate data
engine = create_engine(f'postgresql://{os.environ["DBUSER"]}:{os.environ["DBPW"]}@localhost:5432/hndb')
with engine.begin() as con:
    df = pd.read_sql('SELECT * FROM comments ORDER BY random() LIMIT 5', con=con)
    df = df[df['text'].str.len() != 0]
    df['n_words'] = df['text'].apply(lambda x: len(x.split()))
    df['n_cap'] = df['text'].apply(lambda x: len([word for word in x.split() if word.isupper()]))

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.LUX])
load_figure_template('LUX')


# App layout
app.layout = html.Div([
    html.Div(
        children='My First App with Data'
    ),
    html.Div(
        dash_table.DataTable(
            data=df.to_dict('records'),
            page_size=10,
            style_cell={
                'textOverflow': 'ellipsis',
                'maxWidth': 0
            })
    ),
    html.Div([
        dcc.Dropdown(options=['n_words', 'n_cap'], value='n_words', id='dropdown1'),
        dcc.Graph(figure={}, id='graph1'),
        ], style={'width': '49%', 'display': 'inline-block'}
    ), 
    html.Div([
        dcc.Dropdown(options=['n_words', 'n_cap'], value='n_words', id='dropdown2'),
        dcc.Graph(figure={}, id='graph2'),
        ], style={'width': '49%', 'display': 'inline-block'}
    ),
    ])

# Add controls to build the interaction
@callback(
    Output(component_id='graph1', component_property='figure'),
    Input(component_id='dropdown1', component_property='value')
)
def update_graph1(col_chosen):
    fig = px.scatter(df, x='time', y=col_chosen)
    return fig

@callback(
    Output(component_id='graph2', component_property='figure'),
    Input(component_id='dropdown2', component_property='value')
)
def update_graph2(col_chosen):
    fig = px.scatter(df, x='time', y=col_chosen)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
