import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div("Welcome to the FPL Dashboard!")

if __name__ == "__main__":
    app.run_server(debug=True)