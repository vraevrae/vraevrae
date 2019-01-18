from tempfile import mkdtemp

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

from models.datasource import Datasource
from models.store import Store

store = Store()

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


def answer_question(user_id, answer_id):
    answer = store.get_answer_by_id(answer_id)
    user = store.get_user_by_id(user_id)

    if answer.is_correct:
        question = store.get_question_by_id(answer.question_id)
        user.score += question.score
        return True

    return False


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        username = request.form["username"]

        if request.form["newgame"]:
            if username == "":
                return render_template("index.html", error="Username should not be empty!")

            quiz_id = store.create_quiz(Datasource)
            for _ in range(10):
                store.create_question_from_source(quiz_id)

            user_id = store.create_user(quiz_id=quiz_id, name=username, is_owner=True)

            session["user_id"] = user_id

            return redirect(url_for("game"))

        elif request.form["joingame"]:
            gamecode = request.form["gamecode"]

            if username == "":
                return render_template("index.html", error="Username should not be empty!")
            elif gamecode == "":
                return render_template("index.html", error="Game code should not be empty!")

            quiz = store.get_quiz_by_code(gamecode)
            user_id = store.create_user(quiz_id=quiz.quiz_id, name=username, is_owner=False)

            session["user_id"] = user_id

            return redirect(url_for("game"))


@app.route('/game', methods=["GET", "POST"])
def game():
    if request.method == "GET":
        user = store.get_user_by_id(session["user_id"])
        quiz = store.get_quiz_by_id(user.quiz)

        if not quiz.is_started:
            return render_template("lobby.html", users=store.get_users_by_id(quiz.users), owner=user.is_owner)

        if quiz.is_started and not quiz.is_finished:
            question_id = quiz.get_current_question_id()
            question = store.get_question_by_id(question_id)
            answers = store.get_answers_by_id(question.answers)
            return render_template("quiz.html", question=question, answers=answers)

        if quiz.is_finished:
            return render_template("scoreboard.html", users=store.get_users_by_id(quiz.users))

    elif request.method == "POST":
        action = request.form["action"]
        user = store.get_user_by_id(session["user_id"])

        if action == "start" and user.is_owner:
            store.get_quiz_by_id(user.quiz).start()

            return redirect(url_for("game"))

        elif action == "answer":
            print(request.form)
            answer = store.get_answer_by_id(request.form["answer_id"])

            if answer.is_correct:
                question = store.get_question_by_id(answer.question_id)
                user.score += question.score

            return redirect(url_for("game"))
