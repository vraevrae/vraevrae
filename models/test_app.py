from models.app import App
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
    """questions can be retrieved from the app"""
    app = App()
    quizId = app.createQuiz()
    questionId = app.createQuestion(quizId)
    question = app.getQuestion(questionId)
    assert question

    lcprint(vars(question), "a question:")


def test_create_answer():
    """answers can be added to a app and quiz"""
    app = App()
    quizId = app.createQuiz()
    questionId = app.createQuestion(quizId)
    answerId = app.createAnswer(questionId, "some answer text", True)
    answer = app.answers[answerId]
    assert answer

    lcprint(vars(answer), "a answer:")


def test_get_answer():
    """answers can be retrieved from the app"""
    app = App()
    quizId = app.createQuiz()
    questionId = app.createQuestion(quizId)
    answerId = app.createAnswer(questionId, "some answer text", True)
    answer = app.getAnswer(answerId)
    assert answer

    lcprint(vars(answer), "a answer:")


def test_create_user():
    """users can be added to the app and quiz"""
    app = App()
    quizId = app.createQuiz()
    userId = app.createUser(quizId, {"name": "Someone"})
    user = app.users[userId]
    assert user

    lcprint(vars(user), "a user:")


def test_get_users():
    """users can be retrieved from the app"""
    app = App()
    quizId = app.createQuiz()
    userId = app.createUser(quizId, {"name": "Someone"})
    user = app.getUser(userId)
    assert user

    lcprint(vars(user), "a user:")


def test_filled_app():
    app = App()

    quizCount = 0
    questionCount = 0
    userCount = 0
    answerCount = 0

    for i in range(randint(1, 3)):
        quizId = app.createQuiz()
        quizCount += 1

        for i in range(randint(1, 10)):
            questionId = app.createQuestion(quizId)
            questionCount += 1

            for i in range(randint(2, 4)):
                answerId = app.createAnswer(
                    questionId, "some answer text", True)
                answerCount += 1

        for i in range(randint(1, 10)):
            userId = app.createUser(quizId, {"name": "Someone"})
            userCount += 1

    assert len(app.quizes) == quizCount
    assert len(app.questions) == questionCount
    assert len(app.answers) == answerCount
    assert len(app.users) == userCount

    print("(should be 1)", len(app.quizes))
    print("(should be 2)", len(app.questions))
    print("(should be 6)", len(app.answers))
    print("(should be 7)", len(app.users))

    lcprint(vars(app), "a filled app:")
