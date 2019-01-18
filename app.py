from tempfile import mkdtemp

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

import config
from models import app as quizapp

app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        if request.form["newgame"]:
            if request.form["username"] == "":
                return render_template("index.html", error="Username should not be empty!")

            session["user_id"] = quizapp.App.new_quiz(request.form["username"], config.DEFAULT_DATASOURCE)

            return redirect(url_for("game"))
        elif request.form["joingame"]:
            if request.form["username"] == "":
                return render_template("index.html", error="Username should not be empty!")
            elif request.form["gamecode"] == "":
                return render_template("index.html", error="Game code should not be empty!")

            session["user_id"] = quizapp.App.join_quiz(request.form["username"], request.form["gamecode"])


@app.route('/game', methods=["GET", "POST"])
def game():
    return render_template("quiz.html")


@app.route('/lobby', methods=["GET", "POST"])
def lobby():
    owner=True
    return render_template("lobby.html",
                           users=[{"name": "Username 1", "score": 6590}, {"text": "Username 1", "score": 6590},
                                  {"text": "Username 1", "score": 6590}, {"text": "Username 1", "score": 6590}], owner=owner)


@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    return render_template("quiz.html", question={"text": "What is the biggest planet?"},
                           answers=[{"text": "sun"}, {"text": "jupiter"}])


@app.route('/scoreboard', methods=["GET", "POST"])
def scoreboard():
    return render_template("scoreboard.html",
                           users=[{"name": "Username 1", "score": 6590}, {"text": "Username 1", "score": 6590},
                                  {"text": "Username 1", "score": 6590}, {"text": "Username 1", "score": 6590}])
