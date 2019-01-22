from tempfile import mkdtemp

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

import config
from helpers import helpers
from models.datasource import Datasource
from models.store import Store

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

store = Store()


@app.errorhandler(404)
def error404(e):
    return render_template("404.html"), 404


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        username = request.form.get("username", False)
        if request.form.get("newgame", False):
            # give feedback to user
            if username == "":
                return render_template("index.html", error="Username should not be empty!"), 400

            # create a new game
            quiz_id = store.create_quiz(Datasource)
            for _ in range(10):
                store.create_question_from_source(quiz_id)
            user_id = store.create_user(
                quiz_id=quiz_id, name=username, is_owner=True)
            session["user_id"] = user_id

            return redirect(url_for("game"))

        elif request.form.get("joingame", False):
            gamecode = request.form["gamecode"]

            # give feedback to user
            if username == "":
                return render_template("index.html", error="Username should not be empty!"), 400
            elif gamecode == "":
                return render_template("index.html", error="Game code should not be empty!"), 400

            # join the game
            if store.get_quiz_by_code(gamecode):
                quiz = store.get_quiz_by_code(gamecode)
                user_id = store.create_user(
                    quiz_id=quiz.quiz_id, name=username, is_owner=False)
                session["user_id"] = user_id
                return redirect(url_for("game"))

            # return error
            else:
                return render_template("index.html", error="Game code does not exit!"), 404

        else:
            return render_template("index.html", error="Action is invalid!"), 404


@app.route('/lobby/', methods=["GET", "POST"])
def lobby():
    if request.method == "GET":
        print("[ROUTE] GET /lobby") if config.DEBUG else None

        user = store.get_user_by_id(session["user_id"])
        quiz = store.get_quiz_by_id(user.quiz)

        if not quiz.is_started:
            print("[ROUTE] GET /lobby (QUIZ NOT STARTED)") if config.DEBUG else None
            return render_template("lobby.html", users=store.get_users_by_id(quiz.users),
                                   owner=user.is_owner, gamecode=quiz.code)
        elif quiz.is_started and not quiz.is_finished:
            print(
                "[ROUTE] GET /lobby (QUIZ STARTED -> REDIRECT GAME)") if config.DEBUG else None
            return redirect(url_for("game"))
        elif quiz.is_finished:
            print(
                "[ROUTE] GET /lobby (QUIZ FINISHED -> REDIRECT SCOREBOARD)") if config.DEBUG else None
            return redirect(url_for("scoreboard"))
        else:
            return redirect(url_for(index, error=2))

    elif request.method == "POST":
        print("[ROUTE] POST /lobby") if config.DEBUG else None
        action = request.form["action"]
        user = store.get_user_by_id(session["user_id"])

        if action == "start" and user.is_owner:
            print(
                "[ROUTE] POST /game (ACTION=START AND USER IS OWNER") if config.DEBUG else None
            store.get_quiz_by_id(user.quiz).start()

            return redirect(url_for("game"))


@app.route('/scoreboard/', methods=["GET"])
def scoreboard():
    print("[ROUTE] GET /scoreboard") if config.DEBUG else None

    user = store.get_user_by_id(session["user_id"])
    quiz = store.get_quiz_by_id(user.quiz)

    if not quiz.is_started and not quiz.is_finished:
        print("[ROUTE] GET /lobby (QUIZ NOT STARTED -> REDIRECT INDEX WITH ERROR)") if \
            config.DEBUG else None
        return redirect(url_for("index", error=2))
    elif quiz.is_started and not quiz.is_finished:
        print(
            "[ROUTE] GET /lobby (QUIZ STARTED -> REDIRECT GAME)") if config.DEBUG else None
        return redirect(url_for("game"))
    elif quiz.is_finished:
        print(
            "[ROUTE] GET /scoreboard (QUIZ IS FINISHED") if config.DEBUG else None
        return render_template("scoreboard.html", users=store.get_users_by_id(quiz.users))
    else:
        print("[ROUTE] GET /scoreboard (ELSE -> REDIRECT INDEX WITH ERROR") if config.DEBUG else \
            None
        return redirect(url_for(index, error=2))


@app.route('/game', methods=["GET", "POST"])
@helpers.game_required
def game():
    if request.method == "GET":
        print("[ROUTE] GET /game") if config.DEBUG else None

        user = store.get_user_by_id(session["user_id"])
        quiz = store.get_quiz_by_id(user.quiz)

        if not quiz.is_started:
            print("[ROUTE] GET /game (QUIZ NOT STARTED)") if config.DEBUG else None
            return render_template("lobby.html", users=store.get_users_by_id(quiz.users),
                                   owner=user.is_owner, gamecode=quiz.code)

        if quiz.is_started and not quiz.is_finished:
            print(
                "[ROUTE] GET /game (QUIZ STARTED AND NOT FINISHED)") if config.DEBUG else None
            quiz.next_question()
            question_id = quiz.get_current_question_id()
            question = store.get_question_by_id(question_id)
            answers = store.get_answers_by_id(question.answers)
            print([store.get_question_by_id(question_id).text
                   for question_id in quiz.questions])
            return render_template("quiz.html", question=question, answers=answers)

        if quiz.is_finished:
            print(
                "[ROUTE] GET /game (QUIZ IS FINISHED") if config.DEBUG else None
            return render_template("scoreboard.html", users=store.get_users_by_id(quiz.users))

    elif request.method == "POST":
        print("[ROUTE] POST /game") if config.DEBUG else None
        try:
            action = request.form["action"]
            user = store.get_user_by_id(session["user_id"])
        except KeyError:
            return helpers.json_response()

        if action == "answer":
            print("[ROUTE] POST /game (ACTION=ANSWER") if config.DEBUG else None

            try:
                answer = store.create_user_answer(session["user_id"], request.form["answer_id"])
            except KeyError:
                # TODO KeyError handling! (answer_id)
                pass

            if not answer:
                question = store.get_question_by_id(answer.question_id)
                user.score += question.score

            return redirect(url_for("game"))

        elif action == "start" and user.is_owner:
            print(
                "[ROUTE] POST /game (ACTION=START AND USER IS OWNER") if config.DEBUG else None
            store.get_quiz_by_id(user.quiz).start()

            return redirect(url_for("game"))
