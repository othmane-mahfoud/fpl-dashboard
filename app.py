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
    html.H1("FPL Analytics Dashboard", style={"textAlign": "center"}),
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
                        placeholder="Select Player 1",
                    ),
                ], style={"width": "40%", "margin": "0 10px"}),  # Style for Player 1 dropdown
                html.Div([
                    dcc.Dropdown(
                        id="ict-player2-dropdown",
                        options=[{"label": name, "value": name} for name in ict_index_df["web_name"].unique()],
                        placeholder="Select Player 2",
                    ),
                ], style={"width": "40%", "margin": "0 10px"}),  # Style for Player 2 dropdown
            ], style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "margin-bottom": "20px",
                "gap": "20px",
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
def update_player_performance(player1, player2):
    # Filter data for the two selected players
    filtered_df = player_performance_df[player_performance_df["player_name"].isin([player1, player2])]

    # Compute average performance by gameweek
    avg_df = player_performance_df.groupby("gameweek").agg({"total_points": "mean"}).reset_index()
    avg_df["player_name"] = "Average"

    # Combine the two players' data and the average
    combined_df = pd.concat([filtered_df, avg_df], ignore_index=True)

    # Create the line chart
    fig = px.line(
        combined_df,
        x="gameweek",
        y="total_points",
        color="player_name",
        title="Player Performance by Gameweek",
        labels={"gameweek": "Gameweek", "total_points": "Total Points", "player_name": "Player"},
        line_shape="linear",
    )

    return fig

@app.callback(
    Output("ict-index-chart", "figure"),
    [Input("ict-player1-dropdown", "value"),
     Input("ict-player2-dropdown", "value")]
)
def update_ict_index(player1, player2):
    categories = ["influence", "creativity", "threat", "ict_index"]
    fig = go.Figure()

    if player1:
        # Get metrics for Player 1
        player1_df = ict_index_df[ict_index_df["web_name"] == player1]
        player1_values = player1_df[categories].values[0]
        fig.add_trace(go.Scatterpolar(
            r=player1_values,
            theta=categories,
            fill='toself',
            name=player1,
        ))

    if player2:
        # Get metrics for Player 2
        player2_df = ict_index_df[ict_index_df["web_name"] == player2]
        player2_values = player2_df[categories].values[0]
        fig.add_trace(go.Scatterpolar(
            r=player2_values,
            theta=categories,
            fill='toself',
            name=player2,
        ))

    if not player1 and not player2:
        # Default to average metrics if no players are selected
        avg_values = ict_index_df[categories].mean().values
        fig.add_trace(go.Scatterpolar(
            r=avg_values,
            theta=categories,
            fill='toself',
            name="Average",
        ))

    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(ict_index_df[categories].max()) * 1.2])
        ),
        title="ICT Index Comparison" if player1 or player2 else "Average ICT Index",
        showlegend=True,
    )

    return fig

@app.callback(
    Output("player-cost-performance-chart", "figure"),
    [
        Input("team-dropdown", "value"),
        Input("position-dropdown", "value"),
        Input("budget-dropdown", "value"),
    ]
)
def update_player_cost_performance(selected_team, selected_position, selected_budget):
    # Start with the full dataset
    filtered_df = player_cost_performance_df

    # Apply filters
    if selected_team:
        filtered_df = filtered_df[filtered_df["team_name"] == selected_team]
    if selected_position:
        filtered_df = filtered_df[filtered_df["position"] == selected_position]
    if selected_budget:
        filtered_df = filtered_df[filtered_df["now_cost"] <= selected_budget]

    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x="now_cost",
        y="total_points",
        color="position",
        hover_data=["web_name", "team_name"],
        title="Player Cost vs. Performance",
        labels={"now_cost": "Cost (in 0.1M)", "total_points": "Total Points"},
    )

    return fig


@app.callback(
    Output("fixtures-difficulty-chart", "figure"),
    Input("fixtures-difficulty-chart", "id")  # Placeholder input to trigger rendering
)
def update_fixtures_difficulty(_):
    custom_colorscale = [
        [0, "#00DFA2"],  # Start color
        [1, "#FF0060"]   # End color
    ]

    fig = go.Figure()

    # Add heatmap for home team difficulty
    fig.add_trace(go.Heatmap(
        x=fixtures_difficulty_df["event"],
        y=fixtures_difficulty_df["first_team_name"],
        z=fixtures_difficulty_df["first_team_difficulty"],
        colorscale=custom_colorscale,
        colorbar=dict(title="Fixture Difficulty Rating (FDR)"),
        hovertemplate=(
            "Gameweek: %{x}<br>"
            "Home Team: %{y}<br>"
            "Fixture Difficulty: %{z}<br>"
            "Opponent: %{text}"
        ),
        text=fixtures_difficulty_df["second_team_short_name"],
    ))

    # Layout adjustments
    fig.update_layout(
        title="Fixtures Difficulty Rating by Gameweek",
        xaxis_title="Gameweek",
        yaxis_title="Home Team",
        xaxis=dict(dtick=1, showgrid=False),
        yaxis=dict(showgrid=False),
        font=dict(
            family="Verdana",
            size=12,
            color="#232628"
        ),
        width=800,
        height=600,
        margin=dict(l=100, r=100, t=100, b=100),  # Centering with margins
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)