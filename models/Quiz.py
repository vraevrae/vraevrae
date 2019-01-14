from uuid import uuid4
from models.Question import Question
from models.User import User


class Quiz ():
    "Class that defines the quiz itself"

    def __init__(self):
        quizId = str(uuid4())
        self.quizId = quizId
        self.questions = [Question(quizId) for question in range(10)]
        self.users = [User("somename")]
        self.isStarted = False
        self.isFinished = False
        self.currentQuestion = 0
        self.currentTimer = 0
        self.maxTime = 0

    def addPlayer(self):
        "Adds a player to the quiz"
        print("TODO")

    def getCurrentQuestion():
        "Gets the current question for the quiz"
        print("TODO")

    def checkAnswer(self, questionId, userId):
        "Checks an question and adds the score to the appropriate user"
        print("TODO")

    def nextQuestion(self):
        "Increments the quiz to to the next question"
        print("TODO")

    def finish(self):
        "Ends the quiz"
        print("TODO")
