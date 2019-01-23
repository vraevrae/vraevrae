from flask import url_for, session
import pytest
from app import app, store
from helpers.cprint import lcprint


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
        client = app.test_client()
        data = dict(
            username="pietje",
            newgame="true"
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
            joingame="True"
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
            joingame="True"
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


# def test_answer_question_correctly():
#     app = App()

#     user_id = app.new_quiz("Creator", FakeSource)
#     app.start_quiz(user_id)

#     view = app.get_view(user_id)

#     answer_is_answered = app.answer_question(
#         user_id, view.data["answers"][3].answer_id)

#     assert answer_is_answered

# def test_answer_question_wrongly():
#     app = App()

#     user_id = app.new_quiz("Creator", FakeSource)
#     app.start_quiz(user_id)

#     view = app.get_view(user_id)

#     answer_is_answered = app.answer_question(
#         user_id, view.data["answers"][2].answer_id)

#     assert not answer_is_answered

#     # lcprint(vars(view.data["answers"][2]),
#     #         "the question view with a sepecific answer selected:")
