
from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


# Initialize the app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX])
load_figure_template('LUX')

# Import pages
from pages import page1

# Add controls to build the interaction
page1.register_callbacks(app)

# App layout
app.layout = html.Div([
    page_container
])


# Run the app
if __name__ == '__main__':
    app.run()
