from functools import wraps

from flask import session, redirect, url_for


def game_required(f):
    """
    Decorate routes to require an active game with gamecode.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("index", error=1))
        return f(*args, **kwargs)

    return decorated_function
