from models.app import App
from helpers.fake import FakeSource
from helpers.cprint import cprint, lcprint
from random import randint


def test_create_app():
    """Apps can be created"""
    app = App()
    assert app

    # lcprint(vars(app), "an initialized app:")


def test_app_has_store():
    """Apps have a proper store"""
    app = App()

    assert app.store

    # lcprint(dir(app), "the super class of an app (Store):")


def test_create_quiz():
    """quizes can be created"""
    app = App()
    quiz_id = app.store.create_quiz(FakeSource)
    assert app.store.quizes[quiz_id]

    # lcprint(vars(app), "an app with an quiz:")


def test_get_quiz():
    """quizes can be retrieved from the app"""
    app = App()
    quiz_id = app.store.create_quiz(FakeSource)
    quiz = app.store.get_quiz_by_id(quiz_id)
    assert quiz

    # lcprint(vars(quiz), "a quiz:")


def test_create_question():
    """questions can be added to a app and quiz"""
    app = App()
    quiz_id = app.store.create_quiz(FakeSource)
    question_id = app.store.create_question(
        quiz_id, {"text": "some question", "difficulty": "medium", "category": "some category"})
    question = app.store.questions[question_id]
    assert question

    # lcprint(vars(question), "a question:")


def test_create_question_from_source():
    """questions can be added form a source"""
    app = App()
    quiz_id = app.store.create_quiz(FakeSource)
    question_id = app.store.create_question_from_source(quiz_id)
    question = app.store.questions[question_id]
    assert question

    # lcprint(vars(question), "a question:")


def test_get_question():
    """questions can be retrieved from the app"""
    app = App()
    quiz_id = app.store.create_quiz(FakeSource)
    question_id = app.store.create_question_from_source(quiz_id)
    question = app.store.get_question_by_id(question_id)
    assert question

    # lcprint(vars(question), "a question:")


def test_create_answer():
    """answers can be added to a app and quiz"""
    app = App()
    quiz_id = app.store.create_quiz(FakeSource)
    question_id = app.store.create_question_from_source(quiz_id)
    answer_id = app.store.create_answer(question_id, "some answer text", True)
    answer = app.store.answers[answer_id]
    assert answer

    # lcprint(vars(answer), "a answer:")


def test_get_answer():
    """answers can be retrieved from the app"""
    app = App()
    quiz_id = app.store.create_quiz(FakeSource)
    question_id = app.store.create_question_from_source(quiz_id)
    answer_id = app.store.create_answer(question_id, "some answer text", True)
    answer = app.store.get_answer_by_id(answer_id)
    assert answer

    # lcprint(vars(answer), "a answer:")


def test_create_user():
    """a user can be added to the store and quiz"""
    app = App()
    quiz_id = app.store.create_quiz(FakeSource)
    user_id = app.store.create_user(quiz_id, "Someone",
                                    "BIG-SESSION-TOKEN-ASDFKASLDFGJHKSADNFSAKDFNAS", False)
    user = app.store.users[user_id]
    assert user

    # lcprint(vars(user), "a user:")


def test_get_user_by_id():
    """a user can be retrieved from the app"""
    app = App()
    quiz_id = app.store.create_quiz(FakeSource)
    user_id = app.store.create_user(quiz_id, "Someone",
                                    "BIG-SESSION-TOKEN-ASDFKASLDFGJHKSADNFSAKDFNAS", False)
    user = app.store.get_user_by_id(user_id)
    assert user

    # lcprint(vars(user), "a user:")


def test_get_user_by_session_id():
    """a user can be retrieved from the app"""
    app = App()
    quiz_id = app.store.create_quiz(FakeSource)
    session_token = "BIG-SESSION-TOKEN-ASDFKASLDFGJHKSADNFSAKDFNAS"
    user_id = app.store.create_user(quiz_id, "Someone", session_token, False)
    user = app.store.get_user_by_session_id(session_token)
    assert user


def test_filled_app():
    """Creates a somewhat larger app to test that no extra things are added"""
    app = App()

    quiz_count = 0
    question_count = 0
    user_count = 0

    for _ in range(randint(1, 3)):
        quiz_id = app.store.create_quiz(FakeSource)
        quiz_count += 1

        for _ in range(randint(1, 10)):
            app.store.create_question_from_source(quiz_id)
            question_count += 1

        for _ in range(randint(1, 10)):
            app.store.create_user(quiz_id, "Someone",
                                  "BIG-SESSION-TOKEN", False)
            user_count += 1

    assert len(app.store.quizes) == quiz_count
    assert len(app.store.questions) == question_count
    assert len(app.store.users) == user_count

    # lcprint(vars(app), "a filled app:")


def test_quiz_codes():
    """tests if each quiz has an unique human readable code"""
    app = App()
    app.new_quiz("some name", "BIG-SESSION-TOKEN", FakeSource)
    app.new_quiz("some name", "BIG-SESSION-TOKEN", FakeSource)
    app.new_quiz("some name", "BIG-SESSION-TOKEN", FakeSource)
    app.new_quiz("some name", "BIG-SESSION-TOKEN", FakeSource)
    app.new_quiz("some name", "BIG-SESSION-TOKEN", FakeSource)
    quiz_codes = [quiz.code for quiz in app.store.quizes.values()]

    assert len(quiz_codes) is len(set(quiz_codes))

    # lcprint(quiz_codes, "the quiz codes:")


def test_get_quiz_by_code():
    """tests if a specific quiz can be found by code"""
    app = App()
    quiz_id = app.new_quiz("some name", "BIG-SESSION-TOKEN", FakeSource)
    quiz = app.store.get_quiz_by_id(quiz_id)
    quiz_by_code = app.store.get_quiz_by_code(quiz.code)

    assert quiz_by_code

    # lcprint(vars(quiz_by_code), "the quiz by code:")
