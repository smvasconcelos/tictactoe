from flask import Flask, render_template, request, g
from flask_material import Material
import tictactoe
import json
from waitress import serve
import webbrowser

app = Flask(__name__)
Material(app)

session_data = {}


def is_port_in_use(port):

    """Confere se uma dada porta port está em uso pelo sistema."""
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


@app.route("/")
def home():
    """Rota que inicia a aplicação."""
    template = "home.html"
    return render_template(template)


@app.route("/start_game")
def start_game():

    """Rota responsável por iniciar o jogo."""
    global session_data
    attack = request.args.get("attack")
    if attack == "true":
        attack = True
    else:
        attack = False

    session_data["game"] = tictactoe.Game(attack)

    return session_data["game"].start()


@app.route("/play")
def handle_play():
    """Rota responsável por fazer uma play."""

    global session_data
    play = int(request.args.get("i")), int(request.args.get("j"))
    turn = request.args.get("turn")

    data = session_data["game"].play(play, turn)

    return json.dumps(data)


if __name__ == "__main__":

    if not is_port_in_use(5000):
        webbrowser.open("http://localhost:5000/")
        serve(app, host="0.0.0.0", port=5000)
    else:
        webbrowser.open("http://localhost:5000/")
