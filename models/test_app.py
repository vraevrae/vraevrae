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
    quizId = app.createQuiz(FakeSource)
    assert app.quizes[quizId]

    lcprint(vars(app), "an app with an quiz:")


def test_get_quiz():
    """quizes can be retrieved from the app"""
    app = App()
    quizId = app.createQuiz(FakeSource)
    assert app.getQuiz(quizId)

    lcprint(vars(app.getQuiz(quizId)), "a quiz:")


def test_create_question():
    """questions can be added to a app and quiz"""
    app = App()
    quizId = app.createQuiz(FakeSource)
    questionId = app.createQuestion(
        quizId, {"text": "some question", "difficulty": "medium", "category": "some category"})
    question = app.questions[questionId]
    assert question

    lcprint(vars(question), "a question:")


def test_create_question_from_source():
    """questions can be added form a source"""
    app = App()
    quizId = app.createQuiz(FakeSource)
    questionId = app.createQuestionFromSource(quizId)
    question = app.questions[questionId]
    assert question

    lcprint(vars(question), "a question:")


def test_get_question():
    """questions can be retrieved from the app"""
    app = App()
    quizId = app.createQuiz(FakeSource)
    questionId = app.createQuestionFromSource(quizId)
    question = app.getQuestion(questionId)
    assert question

    lcprint(vars(question), "a question:")


def test_create_answer():
    """answers can be added to a app and quiz"""
    app = App()
    quizId = app.createQuiz(FakeSource)
    questionId = app.createQuestionFromSource(quizId)
    answerId = app.createAnswer(questionId, "some answer text", True)
    answer = app.answers[answerId]
    assert answer

    lcprint(vars(answer), "a answer:")


def test_get_answer():
    """answers can be retrieved from the app"""
    app = App()
    quizId = app.createQuiz(FakeSource)
    questionId = app.createQuestionFromSource(quizId)
    answerId = app.createAnswer(questionId, "some answer text", True)
    answer = app.getAnswer(answerId)
    assert answer

    lcprint(vars(answer), "a answer:")


def test_create_user():
    """users can be added to the app and quiz"""
    app = App()
    quizId = app.createQuiz(FakeSource)
    userId = app.createUser(quizId, "Someone",
                            "BIG-SESSION-TOKEN-ASDFKASLDFGJHKSADNFSAKDFNAS", False)
    user = app.users[userId]
    assert user

    lcprint(vars(user), "a user:")


def test_get_users():
    """users can be retrieved from the app"""
    app = App()
    quizId = app.createQuiz(FakeSource)
    userId = app.createUser(quizId, "Someone",
                            "BIG-SESSION-TOKEN-ASDFKASLDFGJHKSADNFSAKDFNAS", False)
    user = app.getUser(userId)
    assert user

    lcprint(vars(user), "a user:")


def test_filled_app():
    """Creates a somewhat larger app to test that no extra things are added"""
    app = App()

    quizCount = 0
    questionCount = 0
    userCount = 0

    for _ in range(randint(1, 3)):
        quizId = app.createQuiz(FakeSource)
        quizCount += 1

        for _ in range(randint(1, 10)):
            questionId = app.createQuestionFromSource(quizId)
            questionCount += 1

        for _ in range(randint(1, 10)):
            app.createUser(quizId, "Someone",
                           "BIG-SESSION-TOKEN-ASDFKASLDFGJHKSADNFSAKDFNAS", False)
            userCount += 1

    assert len(app.quizes) == quizCount
    assert len(app.questions) == questionCount
    assert len(app.users) == userCount

    lcprint(vars(app), "a filled app:")


def test_new_quiz():
    """Tests the creation of a new default quiz"""
    app = App()
    app.newQuiz("some name", "BIG-SESSION-TOKEN", FakeSource)
    assert True
