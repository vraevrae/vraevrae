from models.app import App
from helpers.fake import FakeSource
from helpers.cprint import cprint, lcprint
from random import randint


def test_new_quiz():
    """creation of a new default quiz"""
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
    """a user can join a quiz by code"""
    app = App()
    quiz_id = app.new_quiz("some creator of the quiz",
                           "BIG-SESSION-TOKEN", FakeSource)
    quiz = app.store.get_quiz_by_id(quiz_id)
    joined_quiz = app.join_quiz(
        "someone who wants to join", "BIG-SESSION-TOKEN", quiz.code)

    assert joined_quiz

    # lcprint(vars(joined_quiz), "the joined quiz:")


def test_start_quiz():
    app = App()
    session_token = "BIG-SESSION-TOKEN"

    quiz_id = app.new_quiz("Creator", session_token, FakeSource)

    quiz_id = app.start_quiz(session_token)

    quiz = app.store.get_quiz_by_id(quiz_id)

    assert quiz.is_started is True

    # lcprint(vars(quiz), "the started quest:")


def test_answer_question_correctly():
    app = App()
    session_token = "BIG-SESSION-TOKEN"

    app.new_quiz("Creator", session_token, FakeSource)
    app.start_quiz(session_token)

    view = app.get_view(session_token)

    answer_is_answered = app.answer_question(
        session_token, view.data["answers"][3].answer_id)

    assert answer_is_answered

    lcprint(vars(view.data["answers"][3]),
            "the question view with a sepecific answer selected:")


def test_answer_question_wrongly():
    app = App()
    session_token = "BIG-SESSION-TOKEN"

    app.new_quiz("Creator", session_token, FakeSource)
    app.start_quiz(session_token)

    view = app.get_view(session_token)

    answer_is_answered = app.answer_question(
        session_token, view.data["answers"][2].answer_id)

    assert not answer_is_answered

    lcprint(vars(view.data["answers"][2]),
            "the question view with a sepecific answer selected:")


def test_next_question():
    app = App()
    session_token = "BIG-SESSION-TOKEN"

    quiz_id = app.new_quiz("Creator", session_token, FakeSource)

    quiz = app.store.get_quiz_by_id(quiz_id)

    quiz.finish()

    assert False
    assert quiz.is_finished is True
    # lcprint(vars(quiz), "the ended quest:")


def test_finish_quiz():
    app = App()
    session_token = "BIG-SESSION-TOKEN"

    quiz_id = app.new_quiz("Creator", session_token, FakeSource)

    quiz = app.store.get_quiz_by_id(quiz_id)

    quiz.finish()

    assert quiz.is_finished is True
    # lcprint(vars(quiz), "the ended quest:")


def test_get_view_lobby():
    app = App()
    session_token = "BIG-SESSION-TOKEN"
    quiz_id = app.new_quiz("some creator of the quiz",
                           session_token, FakeSource)
    view = app.get_view(session_token)

    assert view.type == "lobby"
    assert type(view.data["users"]) is list

    # lcprint(vars(view), "the returned view:")


def test_get_view_question():
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


def test_get_view_scoreboard():
    app = App()
    session_token = "BIG-SESSION-TOKEN"
    quiz_id = app.new_quiz("some creator",
                           session_token, FakeSource)

    quiz_id = app.start_quiz(session_token)
    quiz = app.store.get_quiz_by_id(quiz_id)
    quiz.finish()

    view = app.get_view(session_token)

    assert view.type == "scoreboard"
    assert view.data["users"]

    # lcprint(vars(view), "the returned view:")


def test_next_question_timer():
    assert False
