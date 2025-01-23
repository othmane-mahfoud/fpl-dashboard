from typing import Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_player_performance(player1: str, player2: str, player_performance_df: pd.DataFrame) -> go.Figure:
    """
    Updates the Player Performance chart for the selected players.

    Args:
        player1 (str): The name of the first selected player.
        player2 (str): The name of the second selected player.
        player_performance_df (pd.DataFrame): DataFrame containing player performance data.

    Returns:
        plotly.graph_objects.Figure: A line chart comparing the players' performance across gameweeks.
    """
    try:
        if player_performance_df.empty:
            raise ValueError("Player performance DataFrame is empty.")

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
    except Exception as e:
        logging.error(f"Error updating player performance chart: {e}")
        raise

def update_ict_index(player1: str, player2: str, ict_index_df: pd.DataFrame) -> go.Figure:
    """
    Updates the ICT Index Breakdown radar chart for the selected players.

    Args:
        player1 (str): The name of the first selected player.
        player2 (str): The name of the second selected player.
        ict_index_df (pd.DataFrame): DataFrame containing ICT index data.

    Returns:
        plotly.graph_objects.Figure: A radar chart comparing ICT metrics for the selected players.
    """
    try:
        if ict_index_df.empty:
            raise ValueError("ICT index DataFrame is empty.")

        categories = ["influence", "creativity", "threat", "ict_index"]
        fig = go.Figure()

        if player1:
            # Get metrics for Player 1
            player1_df = ict_index_df[ict_index_df["web_name"] == player1]
            if player1_df.empty:
                raise ValueError(f"Player '{player1}' not found in ICT index data.")
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
            if player2_df.empty:
                raise ValueError(f"Player '{player2}' not found in ICT index data.")
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
    except Exception as e:
        logging.error(f"Error updating ICT index chart: {e}")
        raise

def update_player_cost_performance(
    selected_team: Optional[str],
    selected_position: Optional[str],
    selected_budget: Optional[float],
    player_cost_performance_df: pd.DataFrame,
) -> px.scatter:
    """
    Updates the Player Cost vs. Performance scatter plot based on selected filters.

    Args:
        selected_team (str): The selected team name.
        selected_position (str): The selected player position.
        selected_budget (float): The selected budget limit.
        player_cost_performance_df (pd.DataFrame): DataFrame containing player cost and performance data.

    Returns:
        plotly.graph_objects.Figure: A scatter plot showing player cost vs. performance.
    """
    try:
        if player_cost_performance_df.empty:
            raise ValueError("Player cost vs performance DataFrame is empty.")

        # Start with the full dataset
        filtered_df = player_cost_performance_df

        # Apply filters
        if selected_team:
            filtered_df = filtered_df[filtered_df["team_name"] == selected_team]
        if selected_position:
            filtered_df = filtered_df[filtered_df["position"] == selected_position]
        if selected_budget is not None:
            filtered_df = filtered_df[filtered_df["now_cost"] <= selected_budget]

        if filtered_df.empty:
            raise ValueError("No data matches the selected filters.")

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
    except Exception as e:
        logging.error(f"Error updating player cost vs performance chart: {e}")
        raise

def update_fixtures_difficulty(fixtures_difficulty_df: pd.DataFrame) -> go.Figure:
    """
    Updates the Fixtures Difficulty Rating heatmap.

    Args:
        fixtures_difficulty_df (pd.DataFrame): DataFrame containing fixture difficulty data.

    Returns:
        plotly.graph_objects.Figure: A heatmap showing fixture difficulty ratings by gameweek.
    """
    try:
        if fixtures_difficulty_df.empty:
            raise ValueError("Fixtures difficulty DataFrame is empty.")

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
    except Exception as e:
        logging.error(f"Error updating fixtures difficulty heatmap: {e}")
        raise
