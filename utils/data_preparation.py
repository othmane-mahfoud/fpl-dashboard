import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up paths for CSV files
PLAYERS_CSV = "data/players.csv"
PLAYERS_GW_CSV = "data/players_gw.csv"
FIXTURES_CSV = "data/fixtures.csv"
TEAMS_CSV = "data/teams.csv"

def prepare_player_performance_by_gw(players_gw_path: str, players_path: str) -> pd.DataFrame:
    """
    Prepare data for Player Performance by Gameweek visualization.

    Args:
        players_gw_path (str): Path to the players_gw CSV file.
        players_path (str): Path to the players CSV file.

    Returns:
        pd.DataFrame: Processed DataFrame ready for visualization.
    """
    players_gw_df = pd.read_csv(players_gw_path)
    players_df = pd.read_csv(players_path)

    # Group player gameweek data
    players_gw_df = players_gw_df.groupby(['round', 'element']).agg({
        'total_points': 'sum',
        'minutes': 'sum',
        'goals_scored': 'sum',
        'assists': 'sum',
        'clean_sheets': 'sum'
    }).reset_index()

    # Merge with player names
    merged_df = players_gw_df.merge(players_df[['id', 'web_name']], how='left', left_on='element', right_on='id')

    # Reorder and clean up columns
    merged_df = merged_df[['round', 'web_name', 'total_points', 'minutes', 'goals_scored', 'assists', 'clean_sheets']]
    merged_df.rename(columns={'round': 'gameweek', 'web_name': 'player_name'}, inplace=True)

    return merged_df

def prepare_player_cost_vs_performance(players_path: str, teams_path: str) -> pd.DataFrame:
    """
    Prepare data for Player Cost vs. Performance visualization.

    Args:
        players_path (str): Path to the players CSV file.

    Returns:
        pd.DataFrame: Processed DataFrame ready for visualization.
    """
    players_df = pd.read_csv(players_path)
    players_df = players_df[['web_name', 'element_type', 'team_code', 'now_cost', 'total_points', 'points_per_game']]
    
    teams_df = pd.read_csv(teams_path)
    teams_df = teams_df[['code', 'name']]
    
    # Merge players and teams
    merged_df = players_df.merge(teams_df, how='left', left_on='team_code', right_on='code')

    # Reorder and clean up columns
    merged_df.rename(
        columns={
            'name': 'team_name',
            'element_type': 'position'
        }, inplace=True
    )
    
    # Map player positions
    position_mapping = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}
    merged_df["position"] = merged_df["position"].map(position_mapping)

    return merged_df

def prepare_ict_index_breakdown(players_path: str) -> pd.DataFrame:
    """
    Prepare data for ICT Index Breakdown visualization.

    Args:
        players_path (str): Path to the players CSV file.

    Returns:
        pd.DataFrame: Processed DataFrame ready for visualization.
    """
    df = pd.read_csv(players_path)
    df = df[['web_name', 'influence', 'creativity', 'threat', 'ict_index']]

    return df

def prepare_fixtures_difficulty_ratings(fixtures_path: str, teams_path: str) -> pd.DataFrame:
    """
    Prepare data for Fixtures Difficulty Ratings visualization.

    Args:
        fixtures_path (str): Path to the fixtures CSV file.
        teams_path (str): Path to the teams CSV file.

    Returns:
        pd.DataFrame: Processed DataFrame ready for visualization.
    """
    fixtures_df = pd.read_csv(fixtures_path)
    teams_df = pd.read_csv(teams_path)

    # return fixtures_df
    fixtures_df = pd.merge(fixtures_df, teams_df[['id', 'name', 'short_name']].add_prefix('team_h_'), left_on='team_h', right_on='team_h_id', how='left')
    fixtures_df = pd.merge(fixtures_df, teams_df[['id', 'name', 'short_name']].add_prefix('team_a_'), left_on='team_a', right_on='team_a_id', how='left')
    fixtures_1 = fixtures_df[['event', 'team_h_name', 'team_h_short_name', 'team_h_difficulty', 'team_a_name', 'team_a_short_name', 'team_a_difficulty']]
    fixtures_1 = fixtures_1.rename(columns={
        'event': 'event',
        'team_h_name': 'first_team_name',
        'team_h_short_name': 'first_team_short_name',
        'team_h_difficulty': 'first_team_difficulty',
        'team_a_name': 'second_team_name',
        'team_a_short_name': 'second_team_short_name',
        'team_a_difficulty': 'second_team_difficulty',
    })
    fixtures_2 = fixtures_df[['event', 'team_a_name', 'team_a_short_name', 'team_a_difficulty', 'team_h_name', 'team_h_short_name', 'team_h_difficulty']]
    fixtures_2 = fixtures_2.rename(columns={
        'event': 'event',
        'team_a_name': 'first_team_name',
        'team_a_short_name': 'first_team_short_name',
        'team_a_difficulty': 'first_team_difficulty',
        'team_h_name': 'second_team_name',
        'team_h_short_name': 'second_team_short_name',
        'team_h_difficulty': 'second_team_difficulty',
    })
    fixtures_clean_df = pd.concat([fixtures_1, fixtures_2], ignore_index=True)
    fixtures_clean_df = fixtures_clean_df.sort_values(by='event')
    return fixtures_clean_df

if __name__ == "__main__":
    # Prepare data for visualizations
    logging.info("Preparing Player Performance by Gameweek data...")
    player_performance_df = prepare_player_performance_by_gw(PLAYERS_GW_CSV, PLAYERS_CSV)
    logging.info(f"First rows of Player Performance by Gameweek:\n{player_performance_df.head()}")

    logging.info("Preparing Player Cost vs. Performance data...")
    player_cost_performance_df = prepare_player_cost_vs_performance(PLAYERS_CSV)
    logging.info(f"First rows of Player Cost vs. Performance:\n{player_cost_performance_df.head()}")

    logging.info("Preparing ICT Index Breakdown data...")
    ict_index_df = prepare_ict_index_breakdown(PLAYERS_CSV)
    logging.info(f"First rows of ICT Index Breakdown:\n{ict_index_df.head()}")

    logging.info("Preparing Fixtures Difficulty Ratings data...")
    fixtures_difficulty_df = prepare_fixtures_difficulty_ratings(FIXTURES_CSV, TEAMS_CSV)
    logging.info(f"First rows of Fixtures Difficulty Ratings:\n{fixtures_difficulty_df.head()}")