import requests
import pandas as pd
import os
import logging
from typing import List, Dict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
FPL_BASE_URL = "https://fantasy.premierleague.com/api/"
FPL_BOOTSTRAP_STATIC = FPL_BASE_URL + "bootstrap-static/"
FPL_FIXTURES = FPL_BASE_URL + "fixtures/"
FPL_PLAYER_SUMMARY = FPL_BASE_URL + "element-summary/{player_id}/"

def fetch_data(url: str) -> Dict:
    """
    Fetch data from a given URL.

    Args:
        url (str): API endpoint URL.

    Returns:
        dict: JSON response from the API.

    Raises:
        requests.RequestException: If there is an issue with the HTTP request.
        ValueError: If the response data is invalid or cannot be parsed.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        raise
    except ValueError as ve:
        logging.error(f"Invalid data from {url}: {ve}")
        raise

def fetch_fpl_data() -> Dict:
    """
    Fetch general Fantasy Premier League (FPL) data.

    Returns:
        dict: JSON response containing general FPL data.

    Raises:
        requests.RequestException: If there is an issue with the HTTP request.
        ValueError: If the response data is invalid or cannot be parsed.
    """
    return fetch_data(FPL_BOOTSTRAP_STATIC)

def fetch_fixtures_data() -> List[Dict]:
    """
    Fetch fixtures data.

    Returns:
        list: JSON response containing fixture data.

    Raises:
        requests.RequestException: If there is an issue with the HTTP request.
        ValueError: If the response data is invalid or cannot be parsed.
    """
    return fetch_data(FPL_FIXTURES)

def fetch_player_gw_data(player_id: int) -> List[Dict]:
    """
    Fetch player gameweek data from the Fantasy Premier League API.

    Args:
        player_id (int): Player ID.

    Returns:
        list: List of gameweek data for the player.

    Raises:
        requests.RequestException: If there is an issue with the HTTP request.
        ValueError: If the response data is invalid or cannot be parsed.
    """
    url = FPL_PLAYER_SUMMARY.format(player_id=player_id)
    data = fetch_data(url)
    return data.get('history', [])

def extract_player_details(json_data: Dict) -> pd.DataFrame:
    """
    Extract player details from FPL JSON data.

    Args:
        json_data (dict): JSON data containing player details.

    Returns:
        pd.DataFrame: DataFrame containing player details.

    Raises:
        ValueError: If the JSON data does not contain the 'elements' key or if it is empty.
        Exception: For other errors during data extraction.
    """
    try:
        elements = json_data.get("elements", [])
        if not elements:
            raise ValueError("No 'elements' key found in the data.")
    
        players = [player for player in json_data['elements'] if player['status'] != 'u']
        df = pd.DataFrame(players)

        numeric_columns = ["now_cost", "total_points", "minutes", "goals_scored", "assists"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df
    except Exception as e:
        logging.error(f"Error extracting player details: {e}")
        raise

def extract_active_player_ids(json_data: Dict) -> List[int]:
    """
    Extract IDs of active players from FPL JSON data.

    Args:
        json_data (dict): JSON data containing player details.

    Returns:
        list: List of active player IDs.

    Raises:
        Exception: If there is an issue extracting player IDs.
    """
    try:
        return [player['id'] for player in json_data['elements'] if player['status'] != 'u']
    except Exception as e:
        logging.error(f"Error extracting active player IDs: {e}")
        raise

def extract_player_details_by_gw(player_ids: List[int]) -> pd.DataFrame:
    """
    Extract player gameweek details from the FPL API.

    Args:
        player_ids (list): List of player IDs.

    Returns:
        pd.DataFrame: DataFrame containing gameweek details for players.

    Raises:
        Exception: If there is an issue extracting gameweek details.
    """
    try:
        rows = []
        for player_id in player_ids:
            gw_data = fetch_player_gw_data(player_id)
            rows.extend(gw_data)

        df = pd.DataFrame(rows)
        numeric_columns = ["total_points", "minutes", "goals_scored", "assists"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df
    except Exception as e:
        logging.error(f"Error extracting player details by gameweek: {e}")
        raise

def extract_team_details(json_data: Dict) -> pd.DataFrame:
    """
    Extract team details from FPL JSON data.

    Args:
        json_data (dict): JSON data containing team details.

    Returns:
        pd.DataFrame: DataFrame containing team details.
    """
    df = pd.DataFrame(json_data['teams'])
    numeric_columns = ["strength", "strength_attack_home", "strength_defence_away"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def extract_fixture_details(json_data: List[Dict]) -> pd.DataFrame:
    """
    Extract fixture details from FPL JSON data.

    Args:
        json_data (list): JSON data containing fixture details.

    Returns:
        pd.DataFrame: DataFrame containing fixture details.
    """
    df = pd.DataFrame(json_data)
    selected_columns = [
        "code", "event", "finished", "kickoff_time", "team_a", "team_a_score", "team_h", "team_h_score", "team_h_difficulty", "team_a_difficulty"
    ]
    df = df[selected_columns]
    return df

def save_to_csv(df: pd.DataFrame, output_folder: str, filename: str):
    """
    Save the DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to save.
        output_folder (str): Directory to save the CSV file.
        filename (str): Name of the CSV file.

    Raises:
        OSError: If there is an error creating the output folder or saving the file.
    """
    try:
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(output_folder, filename)
        df.to_csv(file_path, index=False)
        logging.info(f"Data saved to {file_path}")
    except OSError as e:
        logging.error(f"Failed to save {filename}: {e}")
        raise

if __name__ == "__main__":
    OUTPUT_DIR = "data"

    # Fetch data
    logging.info("Fetching FPL data...")
    fpl_data = fetch_fpl_data()
    fixtures_data = fetch_fixtures_data()

    # Extract and save players data
    logging.info("Processing player data...")
    players_df = extract_player_details(fpl_data)
    save_to_csv(players_df, OUTPUT_DIR, "players.csv")

    # Extract and save active player gameweek data
    logging.info("Processing player gameweek data...")
    active_player_ids = extract_active_player_ids(fpl_data)
    players_gw_df = extract_player_details_by_gw(active_player_ids)
    save_to_csv(players_gw_df, OUTPUT_DIR, "players_gw.csv")

    # Extract and save teams data
    logging.info("Processing team data...")
    teams_df = extract_team_details(fpl_data)
    save_to_csv(teams_df, OUTPUT_DIR, "teams.csv")

    # Extract and save fixtures data
    logging.info("Processing fixture data...")
    fixtures_df = extract_fixture_details(fixtures_data)
    save_to_csv(fixtures_df, OUTPUT_DIR, "fixtures.csv")
