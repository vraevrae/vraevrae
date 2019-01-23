from tempfile import mkdtemp

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_session import Session

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

            # return errors
            else:
                return render_template("index.html", error="Game code does not exit!"), 404

        else:
            return render_template("index.html", error="Action is invalid!"), 404


@app.route('/lobby', methods=["GET", "POST"])
def lobby():
    if request.method == "GET":
        user = store.get_user_by_id(session["user_id"])
        quiz = store.get_quiz_by_id(user.quiz)

        if not quiz.is_started:
            return render_template("lobby.html", users=store.get_users_by_id(quiz.users),
                                   owner=user.is_owner, gamecode=quiz.code)
        elif quiz.is_started and not quiz.is_finished:
            return redirect(url_for("game"))
        elif quiz.is_finished:
            return redirect(url_for("scoreboard"))
        else:
            return redirect(url_for(index))

    elif request.method == "POST":
        action = request.form["action"]
        user = store.get_user_by_id(session["user_id"])

        if action == "start" and user.is_owner:
            store.get_quiz_by_id(user.quiz).start()

            return redirect(url_for("game"))

    return redirect(url_for("index")), 400


@app.route('/scoreboard', methods=["GET"])
def scoreboard():
    user = store.get_user_by_id(session["user_id"])
    quiz = store.get_quiz_by_id(user.quiz)

    if not quiz.is_started and not quiz.is_finished:
        return redirect(url_for("index"))
    elif quiz.is_started and not quiz.is_finished:
        return redirect(url_for("game"))
    elif quiz.is_finished:
        return render_template("scoreboard.html", users=store.get_users_by_id(quiz.users))
    else:
        return redirect(url_for(index))


@app.route('/game', methods=["GET", "POST"])
@helpers.game_required
def game():
    if request.method == "GET":
        user = store.get_user_by_id(session["user_id"])
        quiz = store.get_quiz_by_id(user.quiz)

        if not quiz.is_started:
            return render_template("lobby.html", users=store.get_users_by_id(quiz.users),
                                   owner=user.is_owner, gamecode=quiz.code, game_id=quiz.quiz_id)

        if quiz.is_started and not quiz.is_finished:
            quiz.next_question()
            question_id = quiz.get_current_question_id()
            question = store.get_question_by_id(question_id)
            answers = store.get_answers_by_id(question.answers)

            return render_template("quiz.html", question=question, answers=answers)

        if quiz.is_finished:
            return render_template("scoreboard.html", users=store.get_users_by_id(quiz.users))

    elif request.method == "POST":
        try:
            action = request.form["action"]
            user_id = session["user_id"]
            answer_id = request.form["answer_id"]

            if action and user_id and answer_id and action == "answer":
                user = store.get_user_by_id(user_id)
                store.create_user_answer(
                    session["user_id"], request.form["answer_id"])

                answer = store.get_answer_by_id(answer_id)
                if answer.is_correct:
                    question = store.get_question_by_id(answer.question_id)
                    user.score += question.score

                return '', 202

        except:
            return redirect(url_for("index"))


@app.route("/api/<action>/started/<game_id>", methods=["GET"])
def api(action, game_id):
    if action == "game" and game_id:
        try:
            started = store.quizes[game_id].is_started
            finished = store.quizes[game_id].is_finished

            if not started and not finished:
                return jsonify(helpers.json_response({"game_id:": game_id, "has_started": False,
                                                      "has_finished": False})), 200
            elif started and not finished:
                return jsonify(helpers.json_response({"game_id:": game_id, "has_started": True,
                                                      "has_finished": False})), 200
            elif started and finished:
                return jsonify(helpers.json_response({"game_id:": game_id, "has_started": True,
                                                      "has_finished": True})), 200

        except KeyError:
            return jsonify(helpers.json_response({"http_code": 400, "error_message": "game does "
                                                                                     "not "
                                                                                     "exist"})), 400
