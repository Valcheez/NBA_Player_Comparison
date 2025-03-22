from player import Player
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


## use prompt: NBA Player Comparison Layout

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('index.html')

# place error handling here

@app.route("/compare", methods=["POST"])
def compare():
    player1_name = request.form.get("player1")
    player1_season = request.form.get("player1_season") 
    player2_name = request.form.get("player2")
    player2_season = request.form.get("player2_season")

    # trying to add client side form validation, I'll need to eventually add server side validation with html error codes

    error = None
    if request.method == 'POST':
        if not player1_name:
            error = "Invalid player name"
        else:
            pass

    player1 = Player(player1_name, player1_season)
    player2 = Player(player2_name, player2_season)

    # if not player1_name:
    #   print("Error: Player name cannot be empty.")
    #   exit()

    try:
        player1_stats = player1.get_stats()
        player2_stats = player2.get_stats()

        comparison_results ={}
        for stat in player1_stats:
            if stat in player2_stats:
                if player1_stats[stat] > player2_stats[stat]:
                    winner = player1_name
                elif player1_stats[stat] < player2_stats[stat]:
                    winner = player2_name
                else:
                    winner = "Tie"

                comparison_results[stat] = winner

        return render_template(
            "index.html",
            player1_name=player1_name,
            player1_season=player1_season,
            player2_name=player2_name,
            player2_season=player2_season,
            comparison_results=comparison_results,
            winner = winner
        )
    
    except Exception as e:
        return render_template("index.html", error=f"An error occurred: {e}")
    
@app.route("/reset", methods=["GET", "POST"])
def reset():
    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(debug=True)   

# python -m flask run , to run the application

# for debug: set FLASK_DEBUG=1

# I have to add redirects 

# I know my script works. The POST http method is sending data to my flask server which is pretty much my localhost

# I configured "/" route so that now I can use POST requests. Now the compared data/text needs to be updated to the 

# Use form validation(both backend and frontend): flask_wtf for backend. 