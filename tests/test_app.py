from flask import url_for, session
import pytest
from app import app, store
from helpers.cprint import lcprint
from config import DEFAULT_SCORE, MAX_TIME_IN_SECONDS
from time import sleep
from models.quiz import Quiz


def test_app_exists():
    app.testing = True
    assert app


def test_index():
    with app.test_request_context():
        client = app.test_client()
        assert client.get(url_for('index')).status_code == 200


def test_new_quiz():
    """creation of a new default quiz"""

    with app.test_request_context():
        Quiz.max_questions = 2
        Quiz.max_time_in_seconds = 0.1

        client = app.test_client()
        data = dict(
            username="pietje",
            action="newgame"
        )
        rv = client.post(url_for('index'), data=data)

        with client.session_transaction() as sess:
            user_id = sess['user_id']

        quiz = store.get_quiz_by_user_id(user_id)
        question = store.get_question_by_id(quiz.questions[0])
        answer = store.get_answer_by_id(question.answers[0])

    assert quiz
    assert question
    assert answer
    assert user_id in quiz.users
    assert rv.status_code == 302


def test_join_existing_quiz():
    """a user can join a quiz by code"""
    with app.test_request_context():
        client = app.test_client()

        quiz_code = list(store.quizes.values())[0].code

        data = dict(
            username="klaasje",
            gamecode=quiz_code,
            action="joingame"
        )

        rv = client.post(url_for('index'), data=data)

        with client.session_transaction() as sess:
            user_id = sess['user_id']

        quiz = store.get_quiz_by_user_id(user_id)

    assert rv.status_code == 302
    assert user_id in quiz.users


def test_join_non_existing_quiz():
    """a user can join a quiz by code"""
    with app.test_request_context():
        client = app.test_client()
        quiz_code = 39478598347593475
        data = dict(
            username="dirkje",
            gamecode=quiz_code,
            action="joingame"
        )
        rv = client.post(url_for('index'), data=data)

    assert rv.status_code == 404


def test_start_quiz_when_not_owner_yields_error():
    with app.test_request_context():
        client = app.test_client()

        user_id = [user.user_id for user in store.users.values()
                   if user.name == "klaasje"][0]

        with client.session_transaction() as session:
            session['user_id'] = user_id

        rv = client.post(url_for('lobby'), data=dict(
            action="start"
        ))

        quiz = store.get_quiz_by_user_id(user_id)

    assert quiz.is_started is False
    assert not quiz.start_time
    assert rv.status_code == 400


def test_start_quiz_when_owner():
    with app.test_request_context():
        client = app.test_client()

        user_id = [user.user_id for user in store.users.values()
                   if user.name == "pietje"][0]

        with client.session_transaction() as session:
            session['user_id'] = user_id

        rv = client.post(url_for('lobby'), data=dict(
            action="start"
        ))

        quiz = store.get_quiz_by_user_id(user_id)

    assert quiz.is_started is True
    assert quiz.start_time
    assert rv.status_code == 302


def test_answer_question_correctly():
    with app.test_request_context():
        client = app.test_client()

        user_id = [user.user_id for user in store.users.values()
                   if user.name == "pietje"][0]

        with client.session_transaction() as session:
            session['user_id'] = user_id

        quiz = store.get_quiz_by_user_id(user_id)
        question = store.get_question_by_id(quiz.get_current_question_id())
        answers = store.get_answers_by_id(question.answers)
        correct_answer = [answer for answer in answers if answer.is_correct][0]

        rv = client.post(url_for('game'), data=dict(
            action="answer",
            answer_id=correct_answer.answer_id
        ))

        user = store.get_user_by_id(user_id)

        assert rv.status_code == 202
        assert user.score == DEFAULT_SCORE


def test_answer_question_wrongly():
    with app.test_request_context():
        client = app.test_client()

        user_id = [user.user_id for user in store.users.values()
                   if user.name == "klaasje"][0]

        with client.session_transaction() as session:
            session['user_id'] = user_id

        quiz = store.get_quiz_by_user_id(user_id)
        question = store.get_question_by_id(quiz.get_current_question_id())
        answers = store.get_answers_by_id(question.answers)
        correct_answer = [
            answer for answer in answers if not answer.is_correct][0]

        rv = client.post(url_for('game'), data=dict(
            action="answer",
            answer_id=correct_answer.answer_id
        ))

        user = store.get_user_by_id(user_id)

        assert rv.status_code == 202
        assert user.score == 0


def test_quiz_finishes_with_scoreboard():
    with app.test_request_context():

        user_id = [user.user_id for user in store.users.values()
                   if user.name == "pietje"][0]

        client = app.test_client()
        with client.session_transaction() as session:
            session['user_id'] = user_id

        # TODO FIX THIS BUG: Game only increments by 1 for each request (even though it should do more depending on time)
        sleep(0.1)
        rv = client.get(url_for('game'))  # Sets the game to question 2
        sleep(0.1)
        rv = client.get(url_for('game'))  # Sets the game to finished
        sleep(0.1)
        rv = client.get(url_for('game'))  # Finally redirects

        user = store.get_user_by_id(user_id)
        quiz = store.get_quiz_by_user_id(user_id)

        assert rv.status_code == 302
        assert user.score == 10
        assert quiz.is_finished == True
