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
    """Quizes can be created"""
    app = App()
    quizId = app.createQuiz()
    assert app.quizes[quizId]

    print("An app with an quiz:")
    cprint(vars(app))
    print("")


def test_get_quiz():
    """Quizes can be retrieved"""
    app = App()
    quizId = app.createQuiz()
    assert app.getQuiz(quizId)

    print("A quiz:")
    cprint(vars(app.getQuiz(quizId)))
    print("")
