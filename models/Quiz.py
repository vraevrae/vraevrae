from Question import Question
from User import User
from uuid import uuid1
import random
import pprint
import py
pp = pprint.PrettyPrinter(depth=6)


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
        return "TODO"

    def nextQuestion():
        return "TODO"

    def finished():
        return "TODO"


pp.pprint(vars(Quiz()))
