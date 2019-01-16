from models.app import App
from helpers.fake import FakeSource
from helpers.cprint import cprint, lcprint
from random import randint


def test_new_quiz():
    """Tests the creation of a new default quiz"""
    app = App()
    quiz_id = app.new_quiz("some name", "BIG-SESSION-TOKEN", FakeSource)
    quiz = app.store.get_quiz_by_id(quiz_id)

    question = app.store.get_question_by_id(quiz.questions[0])
    answer = app.store.get_answer_by_id(question.answers[0])

    assert quiz
    assert question
    assert answer

    # lcprint(vars(quiz), "a quiz:")
    # lcprint(vars(question), "a question inside the quiz:")
    # lcprint(vars(answer), "a answer inside the question:")


def test_join_quiz():
    """tests if a user can join a quiz by code"""
    app = App()
    quiz_id = app.new_quiz("some creator of the quiz",
                           "BIG-SESSION-TOKEN", FakeSource)
    quiz = app.store.get_quiz_by_id(quiz_id)
    joined_quiz = app.join_quiz(
        "someone who wants to join", "BIG-SESSION-TOKEN", quiz.code)

    assert joined_quiz

    # lcprint(vars(joined_quiz), "the joined quiz:")


def test_get_view_lobby():
    """a user can be retrieved from the app"""
    app = App()
    session_token = "BIG-SESSION-TOKEN"
    quiz_id = app.new_quiz("some creator of the quiz",
                           session_token, FakeSource)
    view = app.get_view(session_token)

    assert view.type == "lobby"
    assert type(view.data["users"]) is list

    # lcprint(vars(view), "the returned view:")


def test_start_quiz():
    app = App()
    session_token = "BIG-SESSION-TOKEN"

    quiz_id = app.new_quiz("Creator", session_token, FakeSource)

    quiz_id = app.start_quiz(session_token)

    # lcprint(vars(app.store.get_quiz_by_id(quiz_id)), "the started quest:")


def test_get_view_question():
    """a user can be retrieved from the app"""
    app = App()
    session_token = "BIG-SESSION-TOKEN"
    quiz_id = app.new_quiz("some creator",
                           session_token, FakeSource)

    quiz_id = app.start_quiz(session_token)
    view = app.get_view(session_token)

    assert view.type == "question"
    assert view.data["question"]
    assert type(view.data["answers"]) is list

    # lcprint(vars(view), "the returned view:")
