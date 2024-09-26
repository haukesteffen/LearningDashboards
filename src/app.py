import os
import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc, callback, Output, Input
from sqlalchemy import create_engine

# Incorporate data
engine = create_engine(f'postgresql://{os.environ["DBUSER"]}:{os.environ["DBPW"]}@localhost:5432/hndb')
with engine.begin() as con:
    df = pd.read_sql('SELECT * FROM comments ORDER BY random() LIMIT 5', con=con)
    df['n_words'] = df['text'].apply(lambda x: len(x.split()))
    df['n_cap'] = df['text'].apply(lambda x: len([word for word in x.split() if word.isupper()]))

# Initialize the app
app = Dash()

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(
        data=df.to_dict('records'),
        page_size=10,
        style_cell={
            'textOverflow': 'ellipsis',
            'maxWidth': 0
        }),
    dcc.Dropdown(options=['n_words', 'n_cap'], value='n_words', id='dropdown'),
    dcc.Graph(figure={}, id='graph')
])

# Add controls to build the interaction
@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
)
def update_graph(col_chosen):
    fig = px.scatter(df, x='time', y=col_chosen)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
