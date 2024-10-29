from flask import Flask, render_template, request, jsonify
from sleeper_wrapper.methods import (
    initialize_league_objects,
    get_users_for_all_leagues,
    get_rosters_for_all_leagues,
    get_matchups_in_all_leagues,
    map_display_names_to_user_ids,
    map_user_ids_to_display_names,
    map_roster_id_to_user_id,
    map_roster_id_to_display_name,
    create_matchup_records,
)
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    try:
        # Get league IDs from the request
        league_ids = request.json.get('league_ids', [])

        app.logger.debug(f"Received League IDs (as strings): {league_ids}")

        # Convert league IDs to integers
        try:
            league_ids = [int(league_id) for league_id in league_ids]
        except ValueError:
            return jsonify({"error": "Invalid league ID format. Must be numeric."}), 400

        app.logger.debug(f"Converted League IDs to integers: {league_ids}")

        # Initialize league objects
        league_objects = initialize_league_objects(league_ids)
        users = get_users_for_all_leagues(league_objects)
        rosters = get_rosters_for_all_leagues(league_objects)
        matchups = get_matchups_in_all_leagues(league_objects)

        # Process data and create matchup records
        display_names_to_user_ids = map_display_names_to_user_ids(users)
        user_id_to_name = map_user_ids_to_display_names(display_names_to_user_ids)
        roster_to_user = map_roster_id_to_user_id(rosters)
        roster_to_name = map_roster_id_to_display_name(user_id_to_name, roster_to_user)
        matchup_records = create_matchup_records(matchups, roster_to_name)

        return jsonify(matchup_records), 200

    except Exception as e:
        import traceback
        app.logger.error(f"Error in /fetch_data: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
