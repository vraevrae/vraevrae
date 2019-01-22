
from tempfile import mkdtemp
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import flask
import pytest
import http

from helpers.fake import FakeSource
from helpers.cprint import cprint, lcprint
from random import randint
from time import sleep

from app import app, store
from models.store import Store


def test_app_exists():
    assert app


def test_index():
    with app.test_request_context():
        client = app.test_client()
        assert client.get(url_for('index')).status_code == 200


def test_new_quiz():
    """creation of a new default quiz"""

    with app.test_request_context():
        client = app.test_client()

        rv = client.post(url_for('index'), data=dict(
            username="pietje",
            newgame="true"
        ))

        user_id = [
            user.user_id for user in store.users.values() if user.name == "pietje"][0]

        quiz = store.get_quiz_by_user_id(user_id)
        question = store.get_question_by_id(quiz.questions[0])
        answer = store.get_answer_by_id(question.answers[0])

    assert quiz
    assert question
    assert answer
    assert rv.status_code == 302


def test_join_quiz():
    """a user can join a quiz by code"""
    with app.test_request_context():
        quiz_code = list(store.quizes.values())[0].code
        client2 = app.test_client()

        data = dict(
            username="klaasje",
            gamecode=quiz_code,
            joingame="True"
        )

        rv = client2.post(url_for('index'), data=data)

        assert rv.status_code == 404

        # user_id = [
        #     user.user_id for user in store.users.values() if user.name == "klaasje"]
        # quiz = store.get_quiz_by_user_id(user_id)

    # user_id_creator = app.new_quiz("some creator of the quiz", FakeSource)
    # quiz = app.store.get_quiz_by_user_id(user_id_creator)
    # user_id_joiner = app.join_quiz("a joiner", quiz.code)

    # assert user_id_joiner

    # lcprint(vars(joined_quiz), "the joined quiz:")

    # def test_start_quiz():
    #     app = App()

    #     user_id = app.new_quiz("Creator", FakeSource)
    #     quiz_id = app.start_quiz(user_id)
    #     quiz = app.store.get_quiz_by_id(quiz_id)

    #     assert quiz.is_started is True
    #     assert quiz.start_time

    #     # lcprint(vars(quiz), "the started quest:")

    # def test_answer_question_correctly():
    #     app = App()

    #     user_id = app.new_quiz("Creator", FakeSource)
    #     app.start_quiz(user_id)

    #     view = app.get_view(user_id)

    #     answer_is_answered = app.answer_question(
    #         user_id, view.data["answers"][3].answer_id)

    #     assert answer_is_answered

    #     # lcprint(vars(view.data["answers"][3]),
    #     #         "the question view with a sepecific answer selected:")

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

    # def test_next_question():
    #     app = App()

    #     user_id = app.new_quiz("Creator", FakeSource)

    #     old_quiz = app.store.get_quiz_by_user_id(user_id)
    #     old_quiz.start()
    #     old_quiz_current_question = old_quiz.current_question
    #     sleep(1.1)
    #     old_quiz.next_question()

    #     new_quiz = app.store.get_quiz_by_user_id(user_id)

    #     assert old_quiz_current_question is new_quiz.current_question - 1

    # def test_next_question_causes_finish():
    #     app = App()

    #     user_id = app.new_quiz("Creator", FakeSource)

    #     quiz = app.store.get_quiz_by_user_id(user_id)
    #     quiz.start()
    #     for _ in range(10):
    #         sleep(1.1)
    #         quiz.next_question()

    #     new_quiz = app.store.get_quiz_by_user_id(user_id)

    #     assert new_quiz.is_finished

    # def test_finish_quiz():
    #     app = App()

    #     user_id = app.new_quiz("Creator", FakeSource)

    #     quiz = app.store.get_quiz_by_user_id(user_id)

    #     quiz.finish()

    #     assert quiz.is_finished is True
    #     # lcprint(vars(quiz), "the ended quest:")

    # def test_get_view_lobby():
    #     app = App()
    #     user_id = app.new_quiz("some creator of the quiz", FakeSource)
    #     view = app.get_view(user_id)

    #     assert view.type == "lobby"
    #     assert type(view.data["users"]) is list

    #     # lcprint(vars(view), "the returned view:")

    # def test_get_view_question():
    #     app = App()
    #     user_id = app.new_quiz("some creator", FakeSource)

    #     app.start_quiz(user_id)
    #     view = app.get_view(user_id)

    #     assert view.type == "question"
    #     assert view.data["question"]
    #     assert type(view.data["answers"]) is list

    #     # lcprint(vars(view), "the returned view:")

    # def test_get_view_scoreboard():
    #     app = App()
    #     user_id = app.new_quiz("some creator", FakeSource)

    #     quiz_id = app.start_quiz(user_id)
    #     quiz = app.store.get_quiz_by_id(quiz_id)
    #     quiz.finish()

    #     view = app.get_view(user_id)

    #     assert view.type == "scoreboard"
    #     assert view.data["users"]

    #     # lcprint(vars(view), "the returned view:")
