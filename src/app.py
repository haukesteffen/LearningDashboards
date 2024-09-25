import os
import pandas as pd
from dash import Dash, html, dash_table
from sqlalchemy import create_engine

# Incorporate data
engine = create_engine(f'postgresql://{os.environ["DBUSER"]}:{os.environ["DBPW"]}@localhost:5432/hndb')
with engine.begin() as con:
    df = pd.read_sql('SELECT * FROM comments ORDER BY random() LIMIT 5', con=con)

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
        })
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
