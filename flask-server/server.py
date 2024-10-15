from flask import Flask, request, jsonify
from sleeper_wrapper import League  # Assuming this is the package you're using

app = Flask(__name__)

@app.route('/api/leaguestats', methods=['GET'])
def get_league_stats():
    league_id = request.args.get('league_id')
    if league_id:
        # Example of using your existing code (you'll need to adapt your logic)
        league = League(league_id)
        matchups = league.get_matchups(1)  # Example for week 1, expand this for your use case

        # Compute wins, losses, and avg points
        stats = {
            'wins': 10,  # Placeholder, compute from matchups
            'losses': 5,  # Placeholder
            'avg_points': 120.5  # Placeholder
        }
        return jsonify(stats)
    else:
        return jsonify({"error": "League ID is required"}), 400

if __name__ == '__main__':
    app.run(debug=True)