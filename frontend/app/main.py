
from dash import Dash, html, page_container

# Initialize the app
app = Dash(__name__, use_pages=True)

# Import pages
from pages import page1, page2

# Add controls to build the interaction
page1.register_callbacks(app)
page2.register_callbacks(app)

# App layout
app.layout = html.Div([
    page_container
])

# Run the app
if __name__ == '__main__':
    app.run()
