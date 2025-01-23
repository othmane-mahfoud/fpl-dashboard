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
    # Create mock CSVs
    players_gw_data = pd.DataFrame({
        "round": [1, 1],
        "element": [1, 2],
        "total_points": [10, 8],
        "minutes": [90, 85],
        "goals_scored": [1, 0],
        "assists": [0, 1],
        "clean_sheets": [1, 0],
    })

    players_data = pd.DataFrame({
        "id": [1, 2],
        "web_name": ["Player 1", "Player 2"],
    })

    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w+", delete=True) as players_gw_csv, \
         tempfile.NamedTemporaryFile(suffix=".csv", mode="w+", delete=True) as players_csv:
        # Write mock data to temporary files
        players_gw_data.to_csv(players_gw_csv.name, index=False)
        players_data.to_csv(players_csv.name, index=False)

        # Run the function
        result = prepare_player_performance_by_gw(players_gw_csv.name, players_csv.name)

        # Validate results
        assert isinstance(result, pd.DataFrame)
        assert "player_name" in result.columns
        assert len(result) == 2


def test_prepare_player_cost_vs_performance():
    # Run the function
    result = prepare_player_cost_vs_performance(MOCK_PLAYERS_CSV, MOCK_TEAMS_CSV)

    # Validate results
    assert isinstance(result, pd.DataFrame)
    assert "team_name" in result.columns
    assert len(result) == 99


def test_prepare_ict_index_breakdown():
    players_data = pd.DataFrame({
        "web_name": ["Player 1"],
        "influence": [100.0],
        "creativity": [50.0],
        "threat": [75.0],
        "ict_index": [225.0],
    })

    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w+", delete=True) as players_csv:
        players_data.to_csv(players_csv.name, index=False)

        # Run the function
        result = prepare_ict_index_breakdown(players_csv.name)

        # Validate results
        assert isinstance(result, pd.DataFrame)
        assert "web_name" in result.columns
        assert len(result) == 1


def test_prepare_fixtures_difficulty_ratings():
    # Run the function
    result = prepare_fixtures_difficulty_ratings(MOCK_FIXTURES_CSV, MOCK_TEAMS_CSV)

    # Validate results
    assert isinstance(result, pd.DataFrame)
    assert "first_team_name" in result.columns
    assert len(result) == 40