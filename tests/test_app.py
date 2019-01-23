from flask import url_for
import pytest
from app import app, store
from helpers.cprint import lcprint


def test_app_exists():
    assert app


@pytest.fixture
def client1():
    with app.test_request_context():
        return app.test_client()


@pytest.fixture
def client2():
    with app.test_request_context():
        return app.test_client()


@pytest.fixture
def client3():
    with app.test_request_context():
        return app.test_client()


def test_index(client1):
    with app.test_request_context():
        assert client1.get(url_for('index')).status_code == 200


def test_new_quiz(client1):
    """creation of a new default quiz"""

    with app.test_request_context():

        rv = client1.post(url_for('index'), data=dict(
            username="pietje",
            newgame="true"
        ))

        with client1.session_transaction() as sess:
            user_id = sess['user_id']

        quiz = store.get_quiz_by_user_id(user_id)
        question = store.get_question_by_id(quiz.questions[0])
        answer = store.get_answer_by_id(question.answers[0])

    assert quiz
    assert question
    assert answer
    assert user_id in quiz.users
    assert rv.status_code == 302


def test_join_existing_quiz(client2):
    """a user can join a quiz by code"""
    with app.test_request_context():
        quiz_code = list(store.quizes.values())[0].code
        data = dict(
            username="klaasje",
            gamecode=quiz_code,
            joingame="True"
        )
        rv = client2.post(url_for('index'), data=data)

        with client2.session_transaction() as sess:
            user_id = sess['user_id']

        quiz = store.get_quiz_by_user_id(user_id)

    assert rv.status_code == 302
    assert user_id in quiz.users


def test_join_non_existing_quiz(client3):
    """a user can join a quiz by code"""
    with app.test_request_context():
        quiz_code = 39478598347593475
        data = dict(
            username="dirkje",
            gamecode=quiz_code,
            joingame="True"
        )
        rv = client3.post(url_for('index'), data=data)

    assert rv.status_code == 404


# def test_start_quiz():
#     with app.test_request_context():
#         lcprint(vars(store))
    # quiz_id = store.start_quiz(user_id)
    # quiz = store.store.get_quiz_by_id(quiz_id)

    # rv = client.post(url_for('lobby'), data=dict(
    #     username="pietje",
    #     newgame="true"
    # ))

    # assert quiz.is_started is True
    # assert quiz.start_time

    # lcprint(vars(quiz), "the started quest:")

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
