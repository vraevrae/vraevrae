from tempfile import mkdtemp

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import time

from helpers.helpers import user_required, game_mode_required
from models.sources.opentdb import OpenTDB
from models.store import store
from models.useranswer import UserAnswer
from config import CATEGORIES
from helpers.cprint import lcprint


app = Flask(__name__)
app.config['SECRET_KEY'] = "extemelysecretvraevraesocketkey"
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)

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


@app.errorhandler(404)
def error404(e):
    return render_template("404.html"), 404


@app.errorhandler(KeyError)
def key_error_page(e):
    return render_template("error.html", data=e), 500


@app.route('/', methods=["GET", "POST"])
def index():
    """route that shows the entry page"""
    if request.method == "GET":
        return render_template("index.html", CATEGORIES=CATEGORIES)

    elif request.method == "POST":
        username = request.form.get("username", False)
        gamecode = request.form.get("gamecode", False)
        action = request.form.get("action", False)
        difficulty = request.form.get("difficulty", None)
        category = request.form.get("category", None)

        if difficulty == "random":
            difficulty = None

        if category == "random":
            category = None

        # give feedback to user
        if username == "":
            return render_template("index.html", error="Username should not be empty!", CATEGORIES=CATEGORIES), 400

        # join the game
        if action == "joingame" and gamecode:
            if store.get_quiz_by_code(gamecode):
                quiz = store.get_quiz_by_code(gamecode)
                user_id = store.create_user(
                    quiz_id=quiz.quiz_id, name=username, is_owner=False)
                session["user_id"] = user_id
                return redirect(url_for("lobby"))
            else:
                return redirect(url_for("index")), 404

        # create a new quiz
        elif action == "creategame":
            # try to make a game (connects to API by instantiating a Datasource)
            # try:
            quiz_id = store.create_quiz(OpenTDB, difficulty, category)
            # except(Exception) as error:
            # return render_template("index.html", error=str(error), CATEGORIES=CATEGORIES), 400

            # create the questions from the Quiz and the Datasource buffer (could connect to API when buffer is empty)
            for _ in range(10):
                store.create_question_from_source(quiz_id)

            # create a user
            user_id = store.create_user(
                quiz_id=quiz_id, name=username, is_owner=True)
            session["user_id"] = user_id

            return redirect(url_for("lobby"))
        # invalid request
        else:
            return "Invalid request", 400


@app.route('/lobby', methods=["GET", "POST"])
@user_required
@game_mode_required
def lobby():
    """route that shows the lobby and receives start game actions"""
    user = store.get_user_by_id(session["user_id"])
    quiz = store.get_quiz_by_id(user.quiz)

    # render the lobby view
    if request.method == "GET":
        users = store.get_users_by_id(quiz.users)
        return render_template("lobby.html", players=users, user=user, quiz=quiz)

    # submit the game start signal
    elif request.method == "POST":
        action = request.form["action"]

        # allow the starting of the quiz if owner
        if action == "start" and user.is_owner:
            # start te quiz
            store.get_quiz_by_id(user.quiz).start()

            # emit to all clients that the game starts (forces a refresh)
            socketio.emit("start_game", room=quiz.quiz_id)

            # redirect the current client
            return redirect(url_for("game"))
        else:
            return "starting quiz only allowed by owner", 400


@app.route('/game', methods=["GET", "POST"])
@user_required
@game_mode_required
def game():
    """route that renders questions and receives answers"""

    # get information
    user_id = session["user_id"]
    user = store.get_user_by_id(user_id)
    quiz = store.get_quiz_by_id(user.quiz)

    # check if it is time to go to the next question, if needed
    quiz.next_question()

    # get question
    question_id = quiz.get_current_question_id()
    question = store.get_question_by_id(question_id)

    if request.method == "GET":
        # retrieve the question and answers
        answers = store.get_answers_by_id(question.answers)

        # get current question (indexed to 1 instead of 0)
        readable_current_question = quiz.current_question + 1

        return render_template("quiz.html", question=question, answers=answers, number=readable_current_question)

    elif request.method == "POST":
        answer_id = request.form["answer_id"]
        answer = store.get_answer_by_id(answer_id)

        # check if enough data to answer the question
        if user_id and answer:

            # get the users answers for this question (user is still scoped to quiz, so user == quiz)
            user_answers = store.get_user_answers_by_user_and_question_id(
                user_id, answer.question_id)

            # if correct and no previous answer found and the question is still active
            if answer.is_correct and not len(user_answers) and answer.question_id == question_id:

                # create a new answer
                new_user_answer = UserAnswer(
                    answer.question_id, answer_id, user_id)

                # store new answer and increment the store
                store.set_user_answer(new_user_answer)
                user.score += question.score
                question = store.get_question_by_id(answer.question_id)

            return f'Accepted answer {answer_id}', 202

        return 'Could not process post request', 400


@app.route('/scoreboard')
@user_required
@game_mode_required
def scoreboard():
    """route that shows the scoreboard"""

    # get data for scoreboard
    user_id = session["user_id"]
    user = store.get_user_by_id(user_id)
    quiz = store.get_quiz_by_id(user.quiz)
    questions = store.get_questions_by_id(quiz.questions)

    # collect and format data for scoreboard
    scoreboard_questions = []
    for question in questions:
        answers = store.get_answers_by_id(question.answers)
        user_answers = store.get_user_answers_by_user_and_question_id(
            user_id, question.question_id)
        answered_answer_id = user_answers[0].answer_id if len(
            user_answers) else False

        scoreboard_question = vars(question)
        scoreboard_question["answers"] = []
        for answer in answers:
            is_chosen = True if answer.answer_id == answered_answer_id else False
            scoreboard_question["answers"].append(
                {**vars(answer), "is_chosen": is_chosen})
            if is_chosen and answer.is_correct:
                scoreboard_question["is_correct"] = True

        scoreboard_questions.append(scoreboard_question)

    return render_template("scoreboard.html", users=store.get_users_by_id(quiz.users), questions=scoreboard_questions)


@socketio.on('connect')
def connect():
    emit('my response')
    print('my response')


@socketio.on("is_connected")
def is_connected(data):
    print(data)


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')


@socketio.on('join_game')
def on_join(data):
    print(data)
    room = data['quiz_id']

    if room is not None:
        join_room(room)
        send(room + ' is joined.', room=room)


@socketio.on('leave_game')
def on_leave(data):
    room = data['quiz_id']
    if room is not None:
        leave_room(room)
        send(room + ' is left.', room=room)
