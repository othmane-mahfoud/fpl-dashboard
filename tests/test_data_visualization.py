from utils.data_visualization import update_player_performance, update_ict_index
import pandas as pd

def test_update_player_performance():
    player_performance_df = pd.DataFrame({
        "gameweek": [1, 1],
        "player_name": ["Player 1", "Player 2"],
        "total_points": [10, 8],
    })
    fig = update_player_performance("Player 1", "Player 2", player_performance_df)
    assert fig.data  # Ensure data exists in the figure
    assert fig.layout.title.text == "Player Performance by Gameweek"

def test_update_ict_index():
    ict_index_df = pd.DataFrame({
        "web_name": ["Player 1", "Player 2"],
        "influence": [100, 50],
        "creativity": [200, 100],
        "threat": [150, 75],
        "ict_index": [450, 225],
    })
    fig = update_ict_index("Player 1", "Player 2", ict_index_df)
    assert fig.data
    assert fig.layout.title.text == "ICT Index Comparison"