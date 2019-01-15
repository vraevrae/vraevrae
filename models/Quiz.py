from uuid import uuid4
from models.Question import Question
from models.User import User
from helpers.fake import apiQuestions


class Quiz ():
    """The central class of the application, nothing happens outside of a quiz"""

    def __init__(self):
        quizId = str(uuid4())
        self.quizId = quizId
        self.questions = [Question(quizId, question)
                          for question in apiQuestions(10)]
        self.users = [User("somename")]
        self.isStarted = False
        self.isFinished = False
        self.currentQuestion = 0
        self.currentTimer = 0
        self.maxTime = 10

    def addPlayer(self):
        """Adds a player to the quiz"""
        # TODO
        print("TODO")

    def getCurrentQuestion(self):
        """Gets the current question for the quiz"""
        # TODO
        print("TODO")

    def checkAnswer(self, questionId, userId):
        """Checks an question and adds the score to the appropriate user"""
        # TODO
        print("TODO")

    def nextQuestion(self):
        """Increments the quiz to to the next question"""
        # TODO
        print("TODO")

    def finish(self):
        """Ends the quiz"""
        # TODO
        print("TODO")
