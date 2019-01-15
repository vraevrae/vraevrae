from models.Quiz import Quiz
from models.Question import Question
from models.User import User
from helpers.fake import apiQuestion


class App ():
    """The application itself, holds the stores and some lookup functions"""

    def __init__(self, **kwargs):
        self.__quizes__ = {}
        self.__questions__ = {}
        self.__answers__ = {}
        self.__users__ = {}

    def createQuiz(self):
        """Creates a new quiz and adds it to the app"""
        newQuiz = Quiz()
        self.__quizes__[newQuiz.quizId] = newQuiz
        self.createQuestion(newQuiz.quizId)

    def readQuiz(self, quizId):
        """read a quiz from the app"""
        return self.__quizes__[quizId]

    def readQuizIds(self):
        """read a quiz from the app"""
        return [quiz for quiz in self.__quizes__]

    def createQuestion(self, quizId):
        """create a new question and add it to the app and to the quiz"""
        newQuestion = Question(**apiQuestion())
        self.readQuiz(quizId).addQuestionById(newQuestion.questionId)
        self.__questions__[newQuestion.questionId] = newQuestion

    def createUser(self, quizId, user):
        """adds a user to the app"""
        newUser = User(**user)
        self.__users__[newUser.userId] = newUser
        self.readQuiz(quizId).addUserById(newUser.userId)

    def readUser(self, userId):
        """Reads a specific user from the app"""
        return self.__users__[userId]

    def readUserIds(self):
        """Reads a list of userIds from the app"""
        return [user for user in self.__users__]
