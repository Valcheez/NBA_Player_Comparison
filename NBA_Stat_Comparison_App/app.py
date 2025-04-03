from flask import Flask, render_template, request, redirect, url_for, flash
from player import Player
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/compare", methods=["POST"])
def compare():
    player1_name = request.form.get("player1", "").strip()
    player2_name = request.form.get("player2", "").strip()
    player1_season = request.form.get("player1_season", "").strip()
    player2_season = request.form.get("player2_season", "").strip()

    errors = []

    if not player1_name:
        errors.append("Player 1 name is required.")
    if not player2_name:
        errors.append("Player 2 name is required.")
    if not player1_season:
        errors.append("Player 1 season is required.")
    if not player2_season:
        errors.append("Player 2 season is required.")


    season_pattern = r'^\d{4}-\d{2}$'
    if player1_season and not re.match(season_pattern, player1_season):
        errors.append("Player 1 season must be in YYYY-YY format.")
    if player2_season and not re.match(season_pattern, player2_season):
        errors.append("Player 2 season must be in YYYY-YY format.")


    if errors:
        for err in errors:
            flash(err, "error")
        return redirect(url_for("home"))
    

    player1_stats = None
    player2_stats = None


    try:
        player1 = Player(player1_name, player1_season)
        player2 = Player(player2_name, player2_season)

        player1_stats = player1.get_stats()
        player2_stats = player2.get_stats()

        if not player1_stats or not player2_stats:
            flash("Could not retrieve stats for one or both players. Check names and seasons.", "error")
            return redirect(url_for("home"))

        comparison_results = {
            stat: player1_name if player1_stats[stat] > player2_stats[stat]
            else player2_name if player1_stats[stat] < player2_stats[stat]
            else "Tie"
            for stat in player1_stats if stat in player2_stats
        }

        return render_template("index.html",
                               comparison_results=comparison_results,
                               player1_name=player1_name,
                               player2_name=player2_name,
                               player1_season=player1_season,
                               player2_season=player2_season)
    
    
    except Exception as e:
        flash(f"Unexpected error: {e}", "error")
        return redirect(url_for("home"))

@app.route("/reset", methods=["GET"])
def reset():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

