import os
import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc
from sqlalchemy import create_engine

# Incorporate data
engine = create_engine(f'postgresql://{os.environ["DBUSER"]}:{os.environ["DBPW"]}@localhost:5432/hndb')
with engine.begin() as con:
    df = pd.read_sql('SELECT * FROM comments ORDER BY random() LIMIT 5', con=con)
    df['n_words'] = df['text'].apply(lambda x: len(x.split()))

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
    dcc.Graph(figure=px.scatter(df, x='time', y='n_words'))
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
