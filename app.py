from tempfile import mkdtemp

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, join_room, emit
from jinja2 import Markup

from config import CATEGORIES
from helpers.helpers import user_required, game_mode_required
from models.sources.opentdb import OpenTDB
from models.store import store
from models.useranswer import UserAnswer

app = Flask(__name__)
app.config['SECRET_KEY'] = "extemelysecretvraevraesocketkey"
app.config['SERVER_NAME'] = None
socketio = SocketIO(app)

app.jinja_env.globals['include_raw'] = lambda filename: Markup(
    app.jinja_loader.get_source(app.jinja_env, filename)[0])

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
    """handle the 404s"""
    return render_template("404.html"), 404


@app.errorhandler(Exception)
def key_error_page(e):
    """handle all kinds of keyerrors"""
    return render_template("index.html", error=e), 500


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
        max_questions = request.form.get("amount", None)

        # give feedback to user
        if username == "":
            return render_template("index.html", error="Username should not be empty!",
                                   CATEGORIES=CATEGORIES), 400

        # join the game
        if action == "joingame" and gamecode:

            # check if gamecode can be case to int
            try:
                gamecode = int(gamecode)
            except ValueError:
                return render_template("index.html", error="Invalid Game Code!", CATEGORIES=CATEGORIES), 400

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

            # if difficulty and category are random, set it to none
            if difficulty == "random":
                difficulty = None

            if category == "random":
                category = None

            # check if max questions can be cast to int
            if max_questions:
                try:
                    max_questions = int(max_questions)
                except TypeError:
                    return render_template("index.html", error="Choose a number between 1 and 50", CATEGORIES=CATEGORIES), 400

                if int(max_questions) < 1 or int(max_questions) > 50:
                    return render_template("index.html", error="Choose a number between 1 and 50", CATEGORIES=CATEGORIES), 400

            # try to make a game (connects to API by instantiating a Datasource)
            quiz_id = store.create_quiz(
                OpenTDB, difficulty, category, max_questions)
            quiz = store.get_quiz_by_id(quiz_id)

            # create the questions from the Quiz and the Datasource buffer (could connect to API
            # when buffer is empty)
            for _ in range(quiz.max_questions):
                store.create_question_from_source(quiz_id)

            # create a user
            user_id = store.create_user(
                quiz_id=quiz_id, name=username, is_owner=True)
            session["user_id"] = user_id

            return redirect(url_for("lobby"))

        elif action == "joingame" and not gamecode:
            return render_template("index.html", error="Game Code should not be empty!",
                                   CATEGORIES=CATEGORIES), 400
        # invalid request
        else:
            # TODO: JOIN GAME WITHOUT CODE EVALUATES TO THIS
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
        # get name of current category
        if quiz.category:
            category = [category["name"] for category in CATEGORIES if int(category["id"]) ==
                        int(quiz.category)][0]
        else:
            category = "Random"

        # render the lobby template (with a vue element for the users included)
        return render_template("lobby.html", user=user, quiz=quiz, category=category)

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


@app.route('/game', methods=["GET"])
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

    # emit finish command so client can reroute
    if quiz.is_finished:
        socketio.emit("finish_game", room=quiz.quiz_id)

    # render template with vue component
    return render_template("quiz.html", user=user, quiz=quiz)


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

        # set user answer id (empty list would evaluate true)
        # TODO: weird that this returns a list of 1, while it should never be more than one
        answered_answer_id = user_answers[0].answer_id if len(
            user_answers) else False

        # format the question
        # make a shallow serializable clone (plain assignment would simply hand over the object pointer)
        scoreboard_question = {**vars(question)}
        scoreboard_question["answers"] = []
        for answer in answers:
            # check if the user actually chose this answer
            is_chosen = True if str(answer.answer_id) == str(
                answered_answer_id) else False
            # append the answers by cloning them and adding a boolean is_chosen
            scoreboard_question["answers"].append(
                {**vars(answer), "is_chosen": is_chosen})
            # TODO: is the question["is_correct"] still used on the client?
            if is_chosen and answer.is_correct:
                scoreboard_question["is_correct"] = True

        scoreboard_questions.append(scoreboard_question)

        # sort users by score
        users = store.get_users_by_id(quiz.users)
        users = sorted(users, key=lambda user: user.score, reverse=True)

    return render_template("scoreboard.html", users=users, questions=scoreboard_questions, quiz=quiz)


@socketio.on('join_game')
def on_join(data):
    """socketio event listener that joins a user and emits to all users if someone joins"""
    quiz = store.get_quiz_by_user_id(data['user_id'])
    room = quiz.quiz_id

    # get and clean the users (no score)
    users = store.get_users_by_id(store.get_quiz_by_id(room).users)
    users_cleaned = [user.name for user in users]

    # emit the new users the to the room
    if room is not None:
        join_room(room)
        emit("current_players", {"users": users_cleaned}, room=room)


@socketio.on('get_current_question')
def get_current_question(data):
    """socketio event listener that emits the current question to the room if so requested"""
    # get the data
    user_id = data["user_id"]
    quiz = store.get_quiz_by_user_id(user_id)

    # check if it is time to go to the next question, if needed
    quiz.next_question()

    if quiz.is_finished:
        socketio.emit("finish_game", room=quiz.quiz_id)

    # get the current question
    question_id = quiz.get_current_question_id()
    question = store.get_question_by_id(question_id)

    # get and clean answers (so client doesn't know which is correct)
    answers = store.get_answers_by_id(question.answers)
    answers_cleaned = [{"answer_id": answer.answer_id, "answer_text": answer.text} for answer in
                       answers]

    # get a minimal quiz object, so client can calculate times
    # TODO: should emit max-time per question to improve time calculation
    quiz_cleaned = {
        "start_time": quiz.start_time.isoformat(),
        "max_questions": quiz.max_questions,
        "max_time_in_seconds": quiz.max_time_in_seconds,
        "current_question": quiz.current_question + 1,
        "total_questions": len(quiz.questions)
    }

    # emit the data
    emit("current_question", {"question": vars(
        question), "answers": answers_cleaned, "quiz": quiz_cleaned}, room=quiz.quiz_id)


@socketio.on('send_answer')
def set_answer(data):
    """socketio event listener that receives an answer from a particular client"""
    # get data
    user_id = data["user_id"]
    user = store.get_user_by_id(user_id)
    answer_id = data["answer_id"]
    answer = store.get_answer_by_id(answer_id)
    quiz = store.get_quiz_by_user_id(user_id)

    # check if it is time to go to the next question, if needed
    quiz.next_question()

    # get the question
    question_id = quiz.get_current_question_id()
    question = store.get_question_by_id(question_id)

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


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
