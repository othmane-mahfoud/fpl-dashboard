import pandas as pd
from utils.data_loading import (
    extract_player_details,
    extract_active_player_ids,
    extract_fixture_details,
)

def test_extract_player_details():
    mock_data = {
        "elements": [
            {"id": 1, "web_name": "Player 1", "now_cost": 50, "total_points": 100, "status": "a"},
            {"id": 2, "web_name": "Player 2", "now_cost": 45, "total_points": 80, "status": "u"},
        ]
    }
    df = extract_player_details(mock_data)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1  # Only active players are included
    assert "now_cost" in df.columns

def test_extract_active_player_ids():
    mock_data = {
        "elements": [
            {"id": 1, "status": "a"},
            {"id": 2, "status": "u"},
            {"id": 3, "status": "a"},
        ]
    }
    active_ids = extract_active_player_ids(mock_data)
    assert active_ids == [1, 3]

def test_extract_fixture_details():
    mock_fixtures = [
        {
            "code": 123,
            "event": 1,
            "finished": True,
            "kickoff_time": "2024-08-16T19:00:00Z",
            "team_a": 9,
            "team_h": 14,
            "team_a_score": 2,
            "team_h_score": 3,
            "team_h_difficulty": 3,
            "team_a_difficulty": 4,
        }
    ]
    df = extract_fixture_details(mock_fixtures)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert "team_h_score" in df.columns