import pandas as pd
import tempfile
from utils.data_preparation import (
    prepare_player_performance_by_gw,
    prepare_player_cost_vs_performance,
    prepare_ict_index_breakdown,
    prepare_fixtures_difficulty_ratings,
)

# Paths to mock files
MOCK_PLAYERS_CSV = "tests/mock_data/mock_players.csv"
MOCK_PLAYERS_GW_CSV = "tests/mock_data/mock_players_gw.csv"
MOCK_FIXTURES_CSV = "tests/mock_data/mock_fixtures.csv"
MOCK_TEAMS_CSV = "tests/mock_data/mock_teams.csv"

def test_prepare_player_performance_by_gw():
    # Run the function
    result = prepare_player_performance_by_gw(MOCK_PLAYERS_GW_CSV, MOCK_PLAYERS_CSV)

    # Validate results
    assert isinstance(result, pd.DataFrame)
    assert "player_name" in result.columns
    assert len(result) == 110


def test_prepare_player_cost_vs_performance():
    # Run the function
    result = prepare_player_cost_vs_performance(MOCK_PLAYERS_CSV, MOCK_TEAMS_CSV)

    # Validate results
    assert isinstance(result, pd.DataFrame)
    assert "team_name" in result.columns
    assert len(result) == 99


def test_prepare_ict_index_breakdown():
    # Run the function
    result = prepare_ict_index_breakdown(MOCK_PLAYERS_CSV)

    # Validate results
    assert isinstance(result, pd.DataFrame)
    assert "web_name" in result.columns
    assert len(result) == 99


def test_prepare_fixtures_difficulty_ratings():
    # Run the function
    result = prepare_fixtures_difficulty_ratings(MOCK_FIXTURES_CSV, MOCK_TEAMS_CSV)

    # Validate results
    assert isinstance(result, pd.DataFrame)
    assert "first_team_name" in result.columns
    assert len(result) == 40