import pytest
import pandas as pd
import plotly.graph_objects as go
from utils.data_visualization import (
    update_player_performance,
    update_ict_index,
    update_player_cost_performance,
    update_fixtures_difficulty
)

def test_update_player_performance():
    # Mock data
    player_performance_df = pd.DataFrame({
        "player_name": ["Player 1", "Player 2", "Player 1", "Player 2"],
        "gameweek": [1, 1, 2, 2],
        "total_points": [10, 12, 15, 20]
    })

    # Test valid inputs
    fig = update_player_performance("Player 1", "Player 2", player_performance_df)
    assert isinstance(fig, go.Figure)

    # Test empty DataFrame
    with pytest.raises(ValueError):
        update_player_performance("Player 1", "Player 2", pd.DataFrame())

def test_update_ict_index():
    # Mock data
    ict_index_df = pd.DataFrame({
        "web_name": ["Player 1", "Player 2"],
        "influence": [10, 15],
        "creativity": [20, 25],
        "threat": [30, 35],
        "ict_index": [60, 75]
    })

    # Test valid inputs
    fig = update_ict_index("Player 1", "Player 2", ict_index_df)
    assert isinstance(fig, go.Figure)

    # Test player not in data
    with pytest.raises(ValueError):
        update_ict_index("Nonexistent Player", "Player 2", ict_index_df)

    # Test empty DataFrame
    with pytest.raises(ValueError):
        update_ict_index("Player 1", "Player 2", pd.DataFrame())

def test_update_player_cost_performance():
    # Mock data
    player_cost_performance_df = pd.DataFrame({
        "web_name": ["Player 1", "Player 2"],
        "now_cost": [50, 45],
        "total_points": [100, 80],
        "team_name": ["Team A", "Team B"],
        "position": ["MID", "FWD"]
    })

    # Test valid inputs
    fig = update_player_cost_performance("Team A", "MID", 50, player_cost_performance_df)
    assert isinstance(fig, go.Figure)

    # Test no matching data
    with pytest.raises(ValueError):
        update_player_cost_performance("Nonexistent Team", "MID", 50, player_cost_performance_df)

    # Test empty DataFrame
    with pytest.raises(ValueError):
        update_player_cost_performance("Team A", "MID", 50, pd.DataFrame())

def test_update_fixtures_difficulty():
    # Mock data
    fixtures_difficulty_df = pd.DataFrame({
        "event": [1, 1, 2, 2],
        "first_team_name": ["Team A", "Team B", "Team A", "Team B"],
        "first_team_difficulty": [3, 4, 2, 5],
        "second_team_short_name": ["B", "A", "B", "A"]
    })

    # Test valid input
    fig = update_fixtures_difficulty(fixtures_difficulty_df)
    assert isinstance(fig, go.Figure)

    # Test empty DataFrame
    with pytest.raises(ValueError):
        update_fixtures_difficulty(pd.DataFrame())