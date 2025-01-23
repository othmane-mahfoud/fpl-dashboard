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

    Raises:
        FileNotFoundError: If input files do not exist.
        ValueError: If required columns are missing.
    """
    try:
        if not os.path.exists(players_gw_path) or not os.path.exists(players_path):
            raise FileNotFoundError("One or more input files are missing.")

        players_gw_df = pd.read_csv(players_gw_path)
        players_df = pd.read_csv(players_path)

        required_columns_gw = ["round", "element", "total_points"]
        if not all(col in players_gw_df.columns for col in required_columns_gw):
            raise ValueError(f"Missing columns in players_gw CSV: {required_columns_gw}")

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

    except (FileNotFoundError, ValueError) as e:
        logging.error(f"Error preparing player performance data: {e}")
        raise

def prepare_player_cost_vs_performance(players_path: str, teams_path: str) -> pd.DataFrame:
    """
    Prepare data for Player Cost vs. Performance visualization.

    Args:
        players_path (str): Path to the players CSV file.
        teams_path (str): Path to the teams CSV file.

    Returns:
        pd.DataFrame: Processed DataFrame ready for visualization.

    Raises:
        FileNotFoundError: If input files do not exist.
        ValueError: If required columns are missing.
    """
    try:
        if not os.path.exists(players_path) or not os.path.exists(teams_path):
            raise FileNotFoundError("One or more input files are missing.")

        players_df = pd.read_csv(players_path)
        teams_df = pd.read_csv(teams_path)

        required_columns_players = ["web_name", "element_type", "team_code", "now_cost", "total_points", "points_per_game"]
        if not all(col in players_df.columns for col in required_columns_players):
            raise ValueError(f"Missing columns in players CSV: {required_columns_players}")

        required_columns_teams = ["code", "name"]
        if not all(col in teams_df.columns for col in required_columns_teams):
            raise ValueError(f"Missing columns in teams CSV: {required_columns_teams}")

        # Merge players and teams
        players_df = players_df[['web_name', 'element_type', 'team_code', 'now_cost', 'total_points', 'points_per_game']]
        teams_df = teams_df[['code', 'name']]

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

    except (FileNotFoundError, ValueError) as e:
        logging.error(f"Error preparing player cost vs performance data: {e}")
        raise

def prepare_ict_index_breakdown(players_path: str) -> pd.DataFrame:
    """
    Prepare data for ICT Index Breakdown visualization.

    Args:
        players_path (str): Path to the players CSV file.

    Returns:
        pd.DataFrame: Processed DataFrame ready for visualization.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If required columns are missing.
    """
    try:
        if not os.path.exists(players_path):
            raise FileNotFoundError("Players CSV file is missing.")

        df = pd.read_csv(players_path)

        required_columns = ["web_name", "influence", "creativity", "threat", "ict_index"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing columns in players CSV: {required_columns}")

        df = df[['web_name', 'influence', 'creativity', 'threat', 'ict_index']]

        return df

    except (FileNotFoundError, ValueError) as e:
        logging.error(f"Error preparing ICT index breakdown data: {e}")
        raise

def prepare_fixtures_difficulty_ratings(fixtures_path: str, teams_path: str) -> pd.DataFrame:
    """
    Prepare data for Fixtures Difficulty Ratings visualization.

    Args:
        fixtures_path (str): Path to the fixtures CSV file.
        teams_path (str): Path to the teams CSV file.

    Returns:
        pd.DataFrame: Processed DataFrame ready for visualization.

    Raises:
        FileNotFoundError: If input files do not exist.
        ValueError: If required columns are missing.
    """
    try:
        if not os.path.exists(fixtures_path) or not os.path.exists(teams_path):
            raise FileNotFoundError("One or more input files are missing.")

        fixtures_df = pd.read_csv(fixtures_path)
        teams_df = pd.read_csv(teams_path)

        required_columns_fixtures = ["team_h", "team_a", "event", "team_h_difficulty", "team_a_difficulty"]
        if not all(col in fixtures_df.columns for col in required_columns_fixtures):
            raise ValueError(f"Missing columns in fixtures CSV: {required_columns_fixtures}")

        required_columns_teams = ["id", "name", "short_name"]
        if not all(col in teams_df.columns for col in required_columns_teams):
            raise ValueError(f"Missing columns in teams CSV: {required_columns_teams}")

        # Merge fixtures with team details
        fixtures_df = pd.merge(fixtures_df, teams_df[['id', 'name', 'short_name']].add_prefix('team_h_'), left_on='team_h', right_on='team_h_id', how='left')
        fixtures_df = pd.merge(fixtures_df, teams_df[['id', 'name', 'short_name']].add_prefix('team_a_'), left_on='team_a', right_on='team_a_id', how='left')

        fixtures_1 = fixtures_df[['event', 'team_h_name', 'team_h_short_name', 'team_h_difficulty', 'team_a_name', 'team_a_short_name', 'team_a_difficulty']].copy()
        fixtures_1.rename(columns={
            'event': 'event',
            'team_h_name': 'first_team_name',
            'team_h_short_name': 'first_team_short_name',
            'team_h_difficulty': 'first_team_difficulty',
            'team_a_name': 'second_team_name',
            'team_a_short_name': 'second_team_short_name',
            'team_a_difficulty': 'second_team_difficulty',
        }, inplace=True)

        fixtures_2 = fixtures_df[['event', 'team_a_name', 'team_a_short_name', 'team_a_difficulty', 'team_h_name', 'team_h_short_name', 'team_h_difficulty']].copy()
        fixtures_2.rename(columns={
            'event': 'event',
            'team_a_name': 'first_team_name',
            'team_a_short_name': 'first_team_short_name',
            'team_a_difficulty': 'first_team_difficulty',
            'team_h_name': 'second_team_name',
            'team_h_short_name': 'second_team_short_name',
            'team_h_difficulty': 'second_team_difficulty',
        }, inplace=True)

        fixtures_clean_df = pd.concat([fixtures_1, fixtures_2], ignore_index=True)
        fixtures_clean_df.sort_values(by='event', inplace=True)

        return fixtures_clean_df

    except (FileNotFoundError, ValueError) as e:
        logging.error(f"Error preparing fixtures difficulty ratings data: {e}")
        raise

if __name__ == "__main__":
    # Prepare data for visualizations
    try:
        logging.info("Preparing Player Performance by Gameweek data...")
        player_performance_df = prepare_player_performance_by_gw(PLAYERS_GW_CSV, PLAYERS_CSV)
        logging.info(f"First rows of Player Performance by Gameweek:\n{player_performance_df.head()}")

        logging.info("Preparing Player Cost vs. Performance data...")
        player_cost_performance_df = prepare_player_cost_vs_performance(PLAYERS_CSV, TEAMS_CSV)
        logging.info(f"First rows of Player Cost vs. Performance:\n{player_cost_performance_df.head()}")

        logging.info("Preparing ICT Index Breakdown data...")
        ict_index_df = prepare_ict_index_breakdown(PLAYERS_CSV)
        logging.info(f"First rows of ICT Index Breakdown:\n{ict_index_df.head()}")

        logging.info("Preparing Fixtures Difficulty Ratings data...")
        fixtures_difficulty_df = prepare_fixtures_difficulty_ratings(FIXTURES_CSV, TEAMS_CSV)
        logging.info(f"First rows of Fixtures Difficulty Ratings:\n{fixtures_difficulty_df.head()}")

    except Exception as e:
        logging.error(f"Error during data preparation: {e}")
