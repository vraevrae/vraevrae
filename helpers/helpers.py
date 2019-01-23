from functools import wraps
from helpers.cprint import lcprint
from flask import session, redirect, url_for, request

from models.store import store


def user_required(f):
    """
    Decorate routes to require an active game with gamecode.
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


def json_response(dictionary=None, ) -> dict:
    return {"data": dictionary}


def game_mode_required(f):
    """checks if game state is appropriate for the route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = store.get_user_by_id(session["user_id"])
        quiz = store.get_quiz_by_id(user.quiz)

        if not quiz.is_started and str(request.url_rule) != "/lobby":
            print("redirecting to lobby")
            return redirect(url_for("lobby"))

        if quiz.is_started and not quiz.is_finished and str(request.url_rule) != "/game":
            print("redirecting to game")
            return redirect(url_for("game"))

        if quiz.is_finished and str(request.url_rule) != "/scoreboard":
            print("redirecting to scoreboard")
            return redirect(url_for("scoreboard"))

        return f(*args, **kwargs)
    return decorated_function
