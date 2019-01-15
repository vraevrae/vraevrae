from uuid import uuid4
from models.Question import Question
from models.User import User


class Quiz ():
    """the central class of the application"""

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
        self.currentTime = 0

    def addQuestionById(self, questionId):
        """adds a question to the quiz"""
        self.questions = [*self.question, questionId]

    def addUserById(self, userId):
        """adds a player to the quiz"""
        self.users = [*self.users, userId]

    def getCurrentQuestion(self):
        """gets the current question for the quiz"""
        # TODO
        pass

    def checkAnswer(self, questionId, userId):
        """asks the question wether the answer is correct, and adds the score to the user"""
        # TODO
        pass

    def nextQuestion(self):
        """increments the quiz to to the next question"""
        # TODO
        pass

    def finish(self):
        """ends the quiz"""
        # TODO
        pass
