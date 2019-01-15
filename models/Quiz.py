from uuid import uuid4
from models.Question import Question
from models.User import User


class Quiz ():
    """The central class of the application, nothing important happens outside of a quiz"""

    # Class attributes, should be the same for all quizes
    maxTime = 10

    # Object attributes, different for each quiz
    def __init__(self, **kwargs):
        self.quizId = str(uuid4())
        self.question = []
        self.users = []
        self.isStarted = False
        self.isFinished = False
        self.isDeleted = False
        self.currentQuestion = ""
        self.currentTimer = 0

    def addQuestionById(self, questionId):
        """Adds a question to the quiz"""
        self.questions = [*self.question, questionId]

    def addUserById(self, userId):
        """Adds a player to the quiz"""
        self.users = [*self.users, userId]

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