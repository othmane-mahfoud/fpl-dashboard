import sys
import os
import dash
import math
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_preparation import (
    prepare_player_performance_by_gw,
    prepare_player_cost_vs_performance,
    prepare_ict_index_breakdown,
    prepare_fixtures_difficulty_ratings,
)
from utils.data_visualization import (
    update_player_performance,
    update_ict_index,
    update_player_cost_performance,
    update_fixtures_difficulty
)

sys.path.insert(0, os.path.abspath('..'))  # Add the project root to sys.path

# CSV Paths
PLAYERS_CSV = "data/players.csv"
PLAYERS_GW_CSV = "data/players_gw.csv"
FIXTURES_CSV = "data/fixtures.csv"
TEAMS_CSV = "data/teams.csv"

# Load processed data
player_performance_df = prepare_player_performance_by_gw(PLAYERS_GW_CSV, PLAYERS_CSV)
player_cost_performance_df = prepare_player_cost_vs_performance(PLAYERS_CSV, TEAMS_CSV)
ict_index_df = prepare_ict_index_breakdown(PLAYERS_CSV)
fixtures_difficulty_df = prepare_fixtures_difficulty_ratings(FIXTURES_CSV, TEAMS_CSV)

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# App layout
app.layout = html.Div([
    html.Div(
        children=[
            html.Img(
                src="assets/pl-main-logo.png",  # Path to the logo file
                style={"height": "80px", "margin-right": "20px"}
            ),
            html.H1(
                "FPL Analytics Dashboard",
                style={"font-family": "Roboto", "margin": "0"}
            ),
        ],
        style={
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
            "margin-bottom": "20px"
        }
    ),
    dcc.Tabs([
        dcc.Tab(label="Player Performance by GW", children=[
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id="player1-dropdown",
                        options=[{"label": name, "value": name} for name in player_performance_df["player_name"].unique()],
                        value="M.Salah",  # Default selection for Player 1
                        placeholder="Select Player 1",
                        style={"width": "100%"},
                    ),
                ], style={"width": "40%", "margin-right": "10px"}),
                html.Div([
                    dcc.Dropdown(
                        id="player2-dropdown",
                        options=[{"label": name, "value": name} for name in player_performance_df["player_name"].unique()],
                        value="Haaland",  # Default selection for Player 2
                        placeholder="Select Player 2",
                        style={"width": "100%"},
                    ),
                ], style={"width": "40%"}),
            ], style={
                "display": "flex",
                "justify-content": "center",
                "gap": "10px",
                "margin-bottom": "20px",
            }),
            dcc.Graph(id="player-performance-chart"),
        ]),
        dcc.Tab(label="Player Cost vs. Performance", children=[
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id="team-dropdown",
                        options=[{"label": team, "value": team} for team in player_cost_performance_df["team_name"].unique()],
                        placeholder="Select Team",
                        style={"width": "100%"},
                    ),
                ], style={"width": "30%", "margin-right": "10px"}),
                html.Div([
                    dcc.Dropdown(
                        id="position-dropdown",
                        options=[{"label": position, "value": position} for position in player_cost_performance_df["position"].unique()],
                        placeholder="Select Position",
                        style={"width": "100%"},
                    ),
                ], style={"width": "30%", "margin-right": "10px"}),
                html.Div([
                    dcc.Dropdown(
                        id="budget-dropdown",
                        options=[{"label": f"{i:.1f} or less", "value": i} for i in range(40, math.ceil(max(player_cost_performance_df["now_cost"])) + 5, 5)],
                        placeholder="Select Budget",
                        style={"width": "100%"},
                    ),
                ], style={"width": "30%"}),
            ], style={
                "display": "flex",
                "justify-content": "center",
                "gap": "10px",
                "margin-bottom": "20px",
            }),
            dcc.Graph(id="player-cost-performance-chart"),
        ]),
        dcc.Tab(label="ICT Index Breakdown", children=[
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id="ict-player1-dropdown",
                        options=[{"label": name, "value": name} for name in ict_index_df["web_name"].unique()],
                        value="M.Salah",  # Default Player 1
                        placeholder="Select Player 1",
                        style={"width": "100%"},
                    ),
                ], style={"width": "40%", "margin-right": "10px"}),
                html.Div([
                    dcc.Dropdown(
                        id="ict-player2-dropdown",
                        options=[{"label": name, "value": name} for name in ict_index_df["web_name"].unique()],
                        value="Haaland",  # Default Player 2
                        placeholder="Select Player 2",
                        style={"width": "100%"},
                    ),
                ], style={"width": "40%"}),
            ], style={
                "display": "flex",
                "justify-content": "center",
                "gap": "10px",
                "margin-bottom": "20px",
                "margin-top": "20px",
            }),
            dcc.Graph(id="ict-index-chart"),
        ]),
        dcc.Tab(label="Fixtures Difficulty Ratings", children=[
            html.Div(
                dcc.Graph(id="fixtures-difficulty-chart"),
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "height": "80vh",  # Center vertically in viewport
                },
            ),
        ]),
    ])
])

# Callbacks
@app.callback(
    Output("player-performance-chart", "figure"),
    [
        Input("player1-dropdown", "value"),
        Input("player2-dropdown", "value"),
    ]
)
def player_performance_callback(player1, player2):
    return update_player_performance(player1, player2, player_performance_df)

@app.callback(
    Output("ict-index-chart", "figure"),
    [Input("ict-player1-dropdown", "value"), Input("ict-player2-dropdown", "value")]
)
def ict_index_callback(player1, player2):
    return update_ict_index(player1, player2, ict_index_df)

@app.callback(
    Output("player-cost-performance-chart", "figure"),
    [
        Input("team-dropdown", "value"),
        Input("position-dropdown", "value"),
        Input("budget-dropdown", "value"),
    ]
)
def player_cost_performance_callback(selected_team, selected_position, selected_budget):
    return update_player_cost_performance(selected_team, selected_position, selected_budget, player_cost_performance_df)

@app.callback(
    Output("fixtures-difficulty-chart", "figure"),
    Input("fixtures-difficulty-chart", "id")
)
def fixtures_difficulty_callback(_):
    return update_fixtures_difficulty(fixtures_difficulty_df)

if __name__ == "__main__":
    # Load processed data
    player_performance_df = prepare_player_performance_by_gw(PLAYERS_GW_CSV, PLAYERS_CSV)
    player_cost_performance_df = prepare_player_cost_vs_performance(PLAYERS_CSV)
    ict_index_df = prepare_ict_index_breakdown(PLAYERS_CSV)
    fixtures_difficulty_df = prepare_fixtures_difficulty_ratings(FIXTURES_CSV, TEAMS_CSV)

    # Run the Dash app
    app.run_server(debug=True)
