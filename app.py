from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "verysecretkeyyesyes"

boggle_game = Boggle()

@app.route("/")
def home():
    session["board"] = boggle_game.make_board()
    if not bool(session.get("highScore")):
        session["highScore"] = 0
    if not bool(session.get("timesPlayed")):
        session["timesPlayed"] = 0
    return render_template("root.html", board = session["board"], highScore = session["highScore"], timesPlayed = session["timesPlayed"])

@app.route("/checkword")
def checkWord():
    guess = request.args["guess"]
    response = boggle_game.check_valid_word(session["board"], guess)
    return jsonify({'result': response})

@app.route("/score", methods = ["POST"])
def score():
    if request.json["score"] > session["highScore"]:
        session["highScore"] = request.json["score"]
    session["timesPlayed"] = session["timesPlayed"] + 1
    return jsonify({'status': 'ok'})