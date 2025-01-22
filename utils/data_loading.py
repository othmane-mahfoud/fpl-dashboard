import requests
import pandas as pd
import os

def fetch_fpl_data():
    """
    Fetch data from the Fantasy Premier League API.

    Returns:
        dict: JSON response containing all FPL data.
    """
    base_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(base_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def fetch_fixtures_data():
    """
    Fetch fixtures data from the Fantasy Premier League API.

    Returns:
        dict: JSON response containing all fixtures data.
    """
    fixtures_url = "https://fantasy.premierleague.com/api/fixtures/"
    response = requests.get(fixtures_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def fetch_player_gw_data(player_id):
    """
    Fetch player gameweek data from the Fantasy Premier League API.

    Args:
        player_id (int): Player ID.
        gw (int): Gameweek number.

    Returns:
        dict: JSON response containing player gameweek data.
    """
    url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    return data['history']

def extract_player_details(json_data):
    """
    Extract player details from the FPL JSON data.

    Args:
        json_data (dict): JSON response from the FPL API.

    Returns:
        pd.DataFrame: DataFrame containing player details.
    """
    rows = []

    for player in json_data['elements']:
        # Check if the player is active
        if player["status"] != "u":
            # Extract all attributes dynamically
            rows.append(player)

    # Convert to DataFrame
    df = pd.DataFrame(rows)

    # Convert data types where applicable
    numeric_columns = [
        "chance_of_playing_next_round", "chance_of_playing_this_round", "cost_change_event",
        "cost_change_event_fall", "cost_change_start", "cost_change_start_fall", "dreamteam_count",
        "element_type", "ep_next", "ep_this", "event_points", "now_cost", "points_per_game",
        "selected_by_percent", "team", "team_code", "total_points", "transfers_in",
        "transfers_in_event", "transfers_out", "transfers_out_event", "minutes", "goals_scored",
        "assists", "clean_sheets", "goals_conceded", "own_goals", "penalties_saved",
        "penalties_missed", "yellow_cards", "red_cards", "saves", "bonus", "bps",
        "influence", "creativity", "threat", "ict_index", "expected_goals", "expected_assists",
        "expected_goal_involvements", "expected_goals_conceded", "starts", "expected_goals_per_90",
        "expected_assists_per_90", "expected_goal_involvements_per_90", "expected_goals_conceded_per_90",
        "goals_conceded_per_90", "now_cost_rank", "now_cost_rank_type", "form_rank",
        "form_rank_type", "points_per_game_rank", "points_per_game_rank_type", "selected_rank",
        "selected_rank_type", "starts_per_90", "clean_sheets_per_90", "saves_per_90"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def extract_active_players_ids(json_data):
    """
    Extract IDs of active players in PL

    Args:
        json_data (dict): JSON response from the FPL API.

    Returns:
        active_players_ids (list): List containing IDs of active players
    """
    active_players_ids = []

    for player in json_data['elements']:
        # Check if the player is active
        if player["status"] != "u":
            # Extract player id
            active_players_ids.append(player["id"])

    return active_players_ids

def extract_player_details_by_gw(player_ids):
    """
    Extract player details for a specific gameweek.

    Args:
        player_ids (list): List of player IDs.
        gw (int): Gameweek number.

    Returns:
        pd.DataFrame: DataFrame containing player details for the specified gameweek.
    """
    rows = []

    for player_id in player_ids:
        player_data = fetch_player_gw_data(player_id)
        for gameweek_data in player_data:
            rows.append(gameweek_data)

    # Convert to DataFrame
    df = pd.DataFrame(rows)

    # Convert data types where applicable
    numeric_columns = [
        "round", "total_points", "minutes", "goals_scored", "assists", "clean_sheets",
        "goals_conceded", "own_goals", "penalties_saved", "penalties_missed", "yellow_cards",
        "red_cards", "saves", "bonus", "bps", "influence", "creativity", "threat", "ict_index"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def extract_team_details(json_data):
    """
    Extract team details from the FPL JSON data.

    Args:
        json_data (dict): JSON response from the FPL API.

    Returns:
        pd.DataFrame: DataFrame containing team details.
    """
    teams = json_data['teams']

    # Convert to DataFrame
    df = pd.DataFrame(teams)

    # Convert data types where applicable
    numeric_columns = [
        "code", "draw", "form", "id", "loss", "played", "points", "position", "strength",
        "team_division", "win", "strength_overall_home", "strength_overall_away",
        "strength_attack_home", "strength_attack_away", "strength_defence_home",
        "strength_defence_away", "pulse_id"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Rename columns for better readability
    df.rename(columns={
        "id": "team_id",
        "short_name": "team_name",
        "strength": "team_strength",
        "strength_overall_home": "team_strength_overall_home",
        "strength_overall_away": "team_strength_overall_away",
        "strength_attack_home": "team_strength_attack_home",
        "strength_attack_away": "team_strength_attack_away",
        "strength_defence_home": "team_strength_defence_home",
        "strength_defence_away": "team_strength_defence_away",
    }, inplace=True)

    return df

def extract_fixture_details(json_data):
    """
    Extract fixture details from the FPL JSON data.

    Args:
        json_data (dict): JSON response from the FPL API.

    Returns:
        pd.DataFrame: DataFrame containing fixture details.
    """
    fixtures = json_data

    # Extract specific attributes
    selected_columns = [
        "code", "event", "finished", "finished_provisional", "id", "kickoff_time",
        "minutes", "provisional_start_time", "started", "team_a", "team_a_score", "team_h", "team_h_score"
    ]

    df = pd.DataFrame(fixtures)[selected_columns]

    # Convert data types where applicable
    numeric_columns = [
        "code", "event", "id", "minutes", "team_a", "team_a_score", "team_h", "team_h_score"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def save_to_csv(df, output_folder="data", filename="output.csv"):
    """
    Save the DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to save.
        output_folder (str): Directory to save the CSV file.
        filename (str): Name of the CSV file.
    """
    os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist
    file_path = os.path.join(output_folder, filename)
    df.to_csv(file_path, index=False)
    print(f"Data successfully saved to {file_path}")

if __name__ == "__main__":
    # Step 1: Fetch FPL data
    fpl_data = fetch_fpl_data()
    fixtures_data = fetch_fixtures_data()

    # Step 2: Extract player details
    players_df = extract_player_details(fpl_data)
    save_to_csv(players_df, filename="players.csv")
    
    # Extract player by gameweek data
    player_ids = extract_active_players_ids(fpl_data)
    players_gw_df = extract_player_details_by_gw(player_ids)
    save_to_csv(players_gw_df, filename="players_gw.csv")

    # Step 3: Extract team details
    teams_df = extract_team_details(fpl_data)
    save_to_csv(teams_df, filename="teams.csv")

    # Step 4: Extract fixture details
    fixtures_df = extract_fixture_details(fixtures_data)
    save_to_csv(fixtures_df, filename="fixtures.csv")