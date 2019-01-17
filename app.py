from tempfile import mkdtemp

from flask import Flask, render_template
from flask_session import Session

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
    return render_template("index.html")


@app.route('/lobby', methods=["GET", "POST"])
def lobby():
    return render_template("lobby.html",
                           users=[{"name": "Username 1", "score": 6590}, {"text": "Username 1", "score": 6590},
                                  {"text": "Username 1", "score": 6590}, {"text": "Username 1", "score": 6590}])


@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    return render_template("quiz.html", question={"text": "What is the biggest planet?"},
                           answers=[{"text": "sun"}, {"text": "jupiter"}])


@app.route('/scoreboard', methods=["GET", "POST"])
def scoreboard():
    return render_template("scoreboard.html",
                           users=[{"name": "Username 1", "score": 6590}, {"text": "Username 1", "score": 6590},
                                  {"text": "Username 1", "score": 6590}, {"text": "Username 1", "score": 6590}])
