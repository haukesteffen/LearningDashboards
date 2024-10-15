
from dash import Dash, html, page_container, dcc

# Initialize the app
app = Dash(__name__, use_pages=True)

# Import pages
from pages import page1, page2, homepage

# Add controls to build the interaction
homepage.register_callbacks(app)
page1.register_callbacks(app)
page2.register_callbacks(app)

# App layout
app.layout = html.Div([
    html.H1(
        dcc.Link('Hacker News Analytics', href='/')
    ),
    page_container
])

# Run the app
if __name__ == '__main__':
    app.run()
