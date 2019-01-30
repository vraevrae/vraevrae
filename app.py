from tempfile import mkdtemp

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from jinja2 import Markup

from config import CATEGORIES, MAX_QUESTIONS
from helpers.helpers import user_required, game_mode_required
from models.sources.opentdb import OpenTDB
from models.store import store
from models.useranswer import UserAnswer
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "extemelysecretvraevraesocketkey"
socketio = SocketIO(app)

app.jinja_env.globals['include_raw'] = lambda filename: Markup(
    app.jinja_loader.get_source(app.jinja_env, filename)[0])

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
        max_questions = request.form.get("amount", MAX_QUESTIONS)

        try:
            max_questions = int(max_questions)
        except ValueError:
            return render_template("index.html", error="Choose a number between 1 and 50", CATEGORIES=CATEGORIES), 400

        if int(max_questions) < 1 or int(max_questions) > 50:
            return render_template("index.html", error="Choose a number between 1 and 50", CATEGORIES=CATEGORIES), 400

        if difficulty == "random":
            difficulty = None

        if category == "random":
            category = None

        # give feedback to user
        if username == "":
            return render_template("index.html", error="Username should not be empty!",
                                   CATEGORIES=CATEGORIES), 400

        # join the game
        if action == "joingame" and gamecode:
            # test if game is already started, if so return an error
            if store.get_quiz_by_code(gamecode) and store.get_quiz_by_code(gamecode).is_started:
                return render_template("index.html", error="Game has already started!",
                                       CATEGORIES=CATEGORIES), 400
            # if game is not started, join game
            elif store.get_quiz_by_code(gamecode):
                quiz = store.get_quiz_by_code(gamecode)
                user_id = store.create_user(
                    quiz_id=quiz.quiz_id, name=username, is_owner=False)
                session["user_id"] = user_id
                return redirect(url_for("lobby"))
            # if game does not exists return a 404
            else:
                return render_template("index.html", error="Game does not exist!",
                                       CATEGORIES=CATEGORIES), 400

        # create a new quiz
        elif action == "creategame":
            # try to make a game (connects to API by instantiating a Datasource)
            quiz_id = store.create_quiz(
                OpenTDB, difficulty, category, max_questions)
            quiz = store.get_quiz_by_id(quiz_id)

            # create the questions from the Quiz and the Datasource buffer (could connect to API when buffer is empty)
            for _ in range(quiz.max_questions or MAX_QUESTIONS):
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
        return render_template("lobby.html", user=user, quiz=quiz)

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

        amount = len(quiz.questions)

        return render_template("quiz.html", user=user, quiz=quiz, question=question, answers=answers, number=readable_current_question, amount=amount)

    elif request.method == "POST":
        answer_id = request.form["answer_id"]
        answer = store.get_answer_by_id(answer_id)

        # check if enough data to answer the question
        if user_id and answer:

            # get the users answers for this question (user is still scoped to quiz, so user == quiz)
            user_answers = store.get_user_answers_by_user_and_question_id(
                user_id, answer.question_id)

            # if correct and no previous answer found and the question is still active
            if not len(user_answers) and answer.question_id == question_id:

                # create a new answer
                new_user_answer = UserAnswer(
                    answer.question_id, answer_id, user_id)

                # store new answer and increment the store
                store.set_user_answer(new_user_answer)
                if answer.is_correct:
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
        # Get answers
        answers = store.get_answers_by_id(question.answers)

        # Get the users answers for the question
        user_answers = store.get_user_answers_by_user_and_question_id(
            user_id, question.question_id)

        # TODO select answers (weird that this returns a list)
        answered_answer_id = user_answers[0].answer_id if len(
            user_answers) else False

        # Format the question
        scoreboard_question = {**vars(question)}
        scoreboard_question["answers"] = []
        for answer in answers:
            is_chosen = True if str(answer.answer_id) == str(
                answered_answer_id) else False
            scoreboard_question["answers"].append(
                {**vars(answer), "is_chosen": is_chosen})
            if is_chosen and answer.is_correct:
                scoreboard_question["is_correct"] = True

        scoreboard_questions.append(scoreboard_question)

    return render_template("scoreboard.html", users=store.get_users_by_id(quiz.users), questions=scoreboard_questions)


@socketio.on('connect')
def connect():
    pass


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
    username = store.get_user_by_id(data["user_id"]).name
    users = [user.name for user in store.get_users_by_id(
        store.get_quiz_by_id(room).users)]

    print(users)

    if room is not None:
        join_room(room)
        emit("current_players", {"users": users}, room=room)


@socketio.on('leave_game')
def on_leave(data):
    room = data['quiz_id']
    if room is not None:
        leave_room(room)
        send(room + ' is left.', room=room)


@socketio.on('get_current_question')
def get_current_question(data):
    print("GET CURRENT QUESTION", data)
    quiz = store.get_quiz_by_id(data["quiz_id"])

    question_id = quiz.get_current_question_id()
    question = store.get_question_by_id(question_id)
    answer_object = store.get_answers_by_id(question.answers)
    answers = [{"answer_id": answer.answer_id, "answer_text": answer.text} for answer in
               answer_object]

    print({"question": question.text, "answers": answers})

    quiz_object = {
        "start_time": quiz.start_time.isoformat(),
        "max_questions": quiz.max_questions,
        "max_time_in_seconds": quiz.max_time_in_seconds
    }

    emit("current_question", {"question": vars(
        question), "answers": answers, "quiz": quiz_object}, room=data["quiz_id"])


@socketio.on('send_answer')
def set_answer(data):
    print("SEND ANSWER", data)
    user_id = data["user_id"]
    answer_id = data["answer_id"]
    quiz_id = data["quiz_id"]
    answer = store.get_answer_by_id(answer_id)
    user = store.get_user_by_id(user_id)
    quiz = store.get_quiz_by_user_id(user_id)
    question_id = quiz.get_current_question_id()
    question = store.get_question_by_id(question_id)

    # check if there is enough data to answer the question
    if user_id and answer:
        print("USER ID AND ANSWER")

        # get the users answers for this question (user is still scoped to quiz, so user ==
        # quiz)
        user_answers = store.get_user_answers_by_user_and_question_id(
            user_id, answer.question_id)

        # if correct and no previous answer found and the question is still active
        if answer.is_correct and len(user_answers) < 1 and answer.question_id == question_id:
            print("ANSWER IS CORRECT")
            # create a new answer
            new_user_answer = UserAnswer(
                answer.question_id, answer_id, user_id)

            # store new answer and increment the store
            store.set_user_answer(new_user_answer)
            user.score += question.score

        # emit that the answer is received by the server
        print("QID -> ", quiz_id)
        print("RID ->", request.sid)

        emit("received_answer", {"success": True,
                                 "user_id": user_id}, room=quiz_id)

    else:
        pass
        # TODO NOT EXCEPTED BY CLIENT return {"success": False, "user_id": user_id}
