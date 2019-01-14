from uuid import uuid1
from models.Question import Question
from models.User import User


class Quiz ():
    "Class that defines the quiz itself"

    def __init__(self):
        quizId = uuid1()
        self.quizId = quizId
        self.questions = [Question(quizId) for question in range(10)]
        self.users = [User("somename")]

    isStarted = False
    activeQuestion = 0

    def addPlayer():
        "Adds a player to the quiz"
        return "TODO"

    def nextQuestion():
        "Increments the quiz to to the next question"
        return "TODO"

    def finished():
        "End the quiz and redirects the players"
        return "TODO"
