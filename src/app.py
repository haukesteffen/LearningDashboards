import requests
from dash import Dash, html, dash_table, dcc, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.LUX])
load_figure_template('LUX')


# App layout
app.layout = html.Div([
    html.Div(
        children='My First App with Dynamic Data'
    ),
    html.Div([
        dcc.Input(id="comment-input", type="text", placeholder="Input Comment ID"),
        dcc.Slider(5, 25, 5,
               value=15,
               id='limit-slider'
        )
    ]),
    html.Div(
        dash_table.DataTable(
            id='comment-table',
            page_size=25,
            style_cell={
                'textOverflow': 'ellipsis',
                'maxWidth': 0
            },
            export_format='csv',
        )
    )
    ])

# Add controls to build the interaction
@app.callback(
    Output('comment-table', 'data'),
    Input('comment-input', 'value'),
    Input('limit-slider', 'value')
)
def display_user_data(comment_id, limit):
    if comment_id:
        # Fetch the selected user's data from FastAPI
        response = requests.get(f"http://localhost:8000/comment/{comment_id}/?limit={limit}")
        if response.status_code == 200:
            comment_data = response.json()
            return comment_data
    return []

# Run the app
if __name__ == '__main__':
    app.run()
