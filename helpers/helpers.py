from functools import wraps

from flask import session, redirect, url_for


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


def game_mode(route, store):
    def game_mode_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = store.get_user_by_id(session["user_id"])
            quiz = store.get_quiz_by_id(user.quiz)
            print("TESSST", quiz.is_finished)

            if not quiz.is_started:
                if route == "lobby":
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for("lobby"))

            if quiz.is_started and not quiz.is_finished:
                if route == "game":
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for("game"))

            if quiz.is_finished:
                if route == "scoreboard":
                    return f(*args, **kwargs)
                else:
                    print("redirecting to scoreboard", quiz.is_finished)
                    return redirect(url_for("scoreboard"))

            return redirect(url_for("index"))

        return decorated_function
    return game_mode_decorator
