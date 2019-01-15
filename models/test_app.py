from models.app import App
from helpers.cprint import cprint, lcprint


def test_create_app():
    """Apps can be created"""
    app = App()
    assert app

    lcprint(vars(app), "an initialized app:")


def test_create_quiz():
    """quizes can be created"""
    app = App()
    quizId = app.createQuiz()
    assert app.quizes[quizId]

    lcprint(vars(app), "an app with an quiz:")


def test_get_quiz():
    """quizes can be retrieved from the app"""
    app = App()
    quizId = app.createQuiz()
    assert app.getQuiz(quizId)

    lcprint(vars(app.getQuiz(quizId)), "a quiz:")


def test_create_question():
    """questions can be added to a app and quiz"""
    app = App()
    quizId = app.createQuiz()
    questionId = app.createQuestion(quizId)
    question = app.questions[questionId]
    assert question

    lcprint(vars(question), "a question:")


def test_get_question():
    """users can be retrieved from the app"""
    app = App()
    quizId = app.createQuiz()
    questionId = app.createQuestion(quizId)
    question = app.getQuestion(questionId)
    assert question

    lcprint(vars(question), "a user:")


def test_create_user():
    """users can be added to the app and quiz"""
    app = App()
    quizId = app.createQuiz()
    userId = app.createUser(quizId, {"name": "Someone"})
    user = app.users[userId]
    assert user

    lcprint(vars(user), "a quiz with a user:")


def test_get_users():
    """users can be retrieved from the app"""
    app = App()
    quizId = app.createQuiz()
    userId = app.createUser(quizId, {"name": "Someone"})
    user = app.getUser(userId)
    assert user

    lcprint(vars(user), "a user:")
