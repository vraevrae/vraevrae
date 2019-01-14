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
        "Voegt een speler aan de quiz toe"
        return "TODO"

    def nextQuestion():
        "Gaat naar de volgende vraagt"
        return "TODO"

    def finished():
        "Sluit de quiz af"
        return "TODO"
