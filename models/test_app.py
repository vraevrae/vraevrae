from models.app import App
from helpers.fake import FakeSource
from helpers.cprint import cprint, lcprint
from random import randint


def test_create_app():
    """Apps can be created"""
    app = App()
    assert app

    lcprint(vars(app), "an initialized app:")


def test_create_quiz():
    """quizes can be created"""
    app = App()
    quiz_id = app.create_quiz(FakeSource)
    assert app.quizes[quiz_id]

    lcprint(vars(app), "an app with an quiz:")


def test_get_quiz():
    """quizes can be retrieved from the app"""
    app = App()
    quiz_id = app.create_quiz(FakeSource)
    quiz = app.get_quiz_by_id(quiz_id)
    assert quiz

    lcprint(vars(quiz), "a quiz:")


def test_create_question():
    """questions can be added to a app and quiz"""
    app = App()
    quiz_id = app.create_quiz(FakeSource)
    question_id = app.create_question(
        quiz_id, {"text": "some question", "difficulty": "medium", "category": "some category"})
    question = app.questions[question_id]
    assert question

    lcprint(vars(question), "a question:")


def test_create_question_from_source():
    """questions can be added form a source"""
    app = App()
    quiz_id = app.create_quiz(FakeSource)
    question_id = app.create_question_from_source(quiz_id)
    question = app.questions[question_id]
    assert question

    lcprint(vars(question), "a question:")


def test_get_question():
    """questions can be retrieved from the app"""
    app = App()
    quiz_id = app.create_quiz(FakeSource)
    question_id = app.create_question_from_source(quiz_id)
    question = app.get_question_by_id(question_id)
    assert question

    lcprint(vars(question), "a question:")


def test_create_answer():
    """answers can be added to a app and quiz"""
    app = App()
    quiz_id = app.create_quiz(FakeSource)
    question_id = app.create_question_from_source(quiz_id)
    answer_id = app.create_answer(question_id, "some answer text", True)
    answer = app.answers[answer_id]
    assert answer

    lcprint(vars(answer), "a answer:")


def test_get_answer():
    """answers can be retrieved from the app"""
    app = App()
    quiz_id = app.create_quiz(FakeSource)
    question_id = app.create_question_from_source(quiz_id)
    answer_id = app.create_answer(question_id, "some answer text", True)
    answer = app.get_answer_by_id(answer_id)
    assert answer

    lcprint(vars(answer), "a answer:")


def test_create_user():
    """users can be added to the app and quiz"""
    app = App()
    quiz_id = app.create_quiz(FakeSource)
    user_id = app.create_user(quiz_id, "Someone",
                              "BIG-SESSION-TOKEN-ASDFKASLDFGJHKSADNFSAKDFNAS", False)
    user = app.users[user_id]
    assert user

    lcprint(vars(user), "a user:")


def test_get_users():
    """users can be retrieved from the app"""
    app = App()
    quiz_id = app.create_quiz(FakeSource)
    user_id = app.create_user(quiz_id, "Someone",
                              "BIG-SESSION-TOKEN-ASDFKASLDFGJHKSADNFSAKDFNAS", False)
    user = app.get_user_by_id(user_id)
    assert user

    lcprint(vars(user), "a user:")


def test_filled_app():
    """Creates a somewhat larger app to test that no extra things are added"""
    app = App()

    quiz_count = 0
    question_count = 0
    user_count = 0

    for _ in range(randint(1, 3)):
        quiz_id = app.create_quiz(FakeSource)
        quiz_count += 1

        for _ in range(randint(1, 10)):
            app.create_question_from_source(quiz_id)
            question_count += 1

        for _ in range(randint(1, 10)):
            app.create_user(quiz_id, "Someone", "BIG-SESSION-TOKEN", False)
            user_count += 1

    assert len(app.quizes) == quiz_count
    assert len(app.questions) == question_count
    assert len(app.users) == user_count

    lcprint(vars(app), "a filled app:")


def test_new_quiz():
    """Tests the creation of a new default quiz"""
    app = App()
    quiz_id = app.new_quiz("some name", "BIG-SESSION-TOKEN", FakeSource)
    quiz = app.get_quiz_by_id(quiz_id)

    lcprint(vars(quiz), "a quiz:")
    question = app.get_question_by_id(quiz.questions[0])
    lcprint(vars(question), "a question inside the quiz:")
    answer = app.get_answer_by_id(question.answers[0])
    lcprint(vars(answer), "a answer inside the question:")

    assert quiz
    assert question
    assert answer
