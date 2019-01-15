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

    maxTime = 10

    def addPlayer(self):
        """Adds a player to the quiz"""
        # TODO
        pass

    def getCurrentQuestion(self):
        """Gets the current question for the quiz"""
        # TODO
        pass

    def checkAnswer(self, questionId, userId):
        """Asks the question wether the answer is correct, and adds the score to the user"""
        # TODO
        pass

    def nextQuestion(self):
        """Increments the quiz to to the next question"""
        # TODO
        pass

    def finish(self):
        """Ends the quiz"""
        # TODO
        pass
