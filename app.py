from tempfile import mkdtemp

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, send, emit

from helpers.helpers import user_required, game_mode_required
from models.datasource import Datasource
from models.store import store

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
        return render_template("index.html")

    elif request.method == "POST":
        username = request.form.get("username", False)
        gamecode = request.form.get("gamecode", False)
        action = request.form.get("action", False)

        # give feedback to user
        if username == "":
            return render_template("index.html", error="Username should not be empty!"), 400

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

        else:
            quiz_id = store.create_quiz(Datasource)
            for _ in range(10):
                if action == "easy":
                    question_id = store.create_question_from_source(quiz_id, difficulty="easy")
                if action == "medium":
                    question_id = store.create_question_from_source(quiz_id, difficulty="medium")
                if action == "hard":
                    question_id = store.create_question_from_source(quiz_id, difficulty="hard")
                else:
                    question_id = store.create_question_from_source(quiz_id)
                
                print(vars(store.get_question_by_id(question_id)))


            # create a user
            user_id = store.create_user(
                quiz_id=quiz_id, name=username, is_owner=True)
            session["user_id"] = user_id

            return redirect(url_for("lobby"))


@app.route('/lobby', methods=["GET", "POST"])
@user_required
@game_mode_required
def lobby():
    """route that shows the lobby and receives start game actions"""
    user = store.get_user_by_id(session["user_id"])

    # render the lobby view
    if request.method == "GET":
        quiz = store.get_quiz_by_id(user.quiz)
        users = store.get_users_by_id(quiz.users)
        return render_template("lobby.html", players=users, user=user, quiz=quiz)

    # submit the game start signal
    elif request.method == "POST":
        action = request.form["action"]

        # allow the starting of th quiz if owner
        if action == "start" and user.is_owner:
            store.get_quiz_by_id(user.quiz).start()
            socketio.emit("start_game", room=store.get_quiz_by_id(user.quiz).quiz_id)

            return redirect(url_for("game"))
        else:
            return "starting quiz only allowed by owner", 400


@app.route('/game', methods=["GET", "POST"])
@user_required
@game_mode_required
def game():
    """route that renders questions and receives answers"""
    # go the the next question (if needed)
    user = store.get_user_by_id(session["user_id"])
    quiz = store.get_quiz_by_id(user.quiz)
    quiz.next_question()

    if request.method == "GET":
        # retrieve the question and answers
        question_id = quiz.get_current_question_id()
        question = store.get_question_by_id(question_id)
        answers = store.get_answers_by_id(question.answers)

        return render_template("quiz.html", question=question, answers=answers)

    elif request.method == "POST":
        user_id = session["user_id"]
        answer_id = request.form["answer_id"]

        if user_id and answer_id:
            # create history item
            store.create_user_answer(user_id, answer_id)

            # check for correctness (and increment score if needed)
            answer = store.get_answer_by_id(answer_id)
            if answer.is_correct:
                question = store.get_question_by_id(answer.question_id)
                user = store.get_user_by_id(user_id)
                user.score += question.score

            return '', 202


@app.route('/scoreboard')
@user_required
@game_mode_required
def scoreboard():
    """route that shows the scoreboard"""
    # get data for scoreboard
    user = store.get_user_by_id(session["user_id"])
    quiz = store.get_quiz_by_id(user.quiz)
    return render_template("scoreboard.html", users=store.get_users_by_id(quiz.users))


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
    leave_room(room)
    send(room + ' is left.', room=room)
