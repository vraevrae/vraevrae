from functools import wraps

from flask import session, redirect, url_for, request

from models.store import store


def user_required(f):
    """only render the route if there is a user session"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if not user redirect
        if session.get("user_id") is None:
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


def game_mode_required(f):
    """checks if game state is appropriate for the route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # get quiz data
        user = store.get_user_by_id(session["user_id"])
        quiz = store.get_quiz_by_id(user.quiz)

        # game mode = preparation
        if not quiz.is_started and str(request.url_rule) != "/lobby":
            return redirect(url_for("lobby"))

        # game mode = active
        if quiz.is_started and not quiz.is_finished and str(request.url_rule) != "/game":
            return redirect(url_for("game"))

        # game mode = finished
        if quiz.is_finished and str(request.url_rule) != "/scoreboard":
            return redirect(url_for("scoreboard"))

        # if on correct route, return the route function
        return f(*args, **kwargs)
    return decorated_function


def json_response(dictionary=None) -> dict:
    # create response template for json
    return {"data": dictionary}
