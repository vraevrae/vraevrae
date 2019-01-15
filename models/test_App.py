from models.App import App
from helpers.cprint import cprint


def test_create_app():
    """Apps can be created"""
    app = App()
    assert app

    print("An initialized app:")
    cprint(vars(app))
    print("")


def test_create_quiz():
    """quizes can be created"""
    app = App()
    quizId = app.createQuiz()
    assert app.quizes[quizId]

    print("An app with an quiz:")
    cprint(vars(app))
    print("")


def test_get_quiz():
    """quizes can be retrieved from the app"""
    app = App()
    quizId = app.createQuiz()
    assert app.getQuiz(quizId)

    print("A quiz:")
    cprint(vars(app.getQuiz(quizId)))
    print("")


def test_create_question():
    """questions can be added to a app and quiz"""
    app = App()
    quizId = app.createQuiz()
    questionId = app.createQuestion(quizId)
    question = app.questions[questionId]
    assert question

    print("A question:")
    cprint(vars(question))
    print("")


def test_create_user():
    """users can be added to the app and quiz"""
    app = App()
    quizId = app.createQuiz()
    userId = app.createUser(quizId, {"name": "Someone"})
    user = app.users[userId]
    assert user

    print("A quiz with a user:")
    cprint(vars(user))


def test_get_users():
    """users can be retrieved from the app"""
    firstUserId = list(app.users.values())[0].userId
    print("A user:")
    cprint(vars(app.getUser(firstUserId)))
