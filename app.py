from flask import Flask, render_template, request, g
from flask_material import Material
import tictactoe
import json

app = Flask(__name__)
Material(app)

session_data = {}


@app.route("/")
def home():

    template = "home.html"
    return render_template(template)


@app.route("/start_game")
def start_game():

    global session_data
    attack = request.args.get("attack")
    if attack == "True":
        attack = True
    else:
        attack = False

    session_data["game"] = tictactoe.Game(attack)

    return session_data["game"].start()


@app.route("/play")
def handle_play():

    global session_data
    play = int(request.args.get("i")), int(request.args.get("j"))
    turn = request.args.get("turn")

    data = session_data["game"].play(play, turn)

    return json.dumps(data)


if __name__ == "__main__":

    app.run(debug=True)
