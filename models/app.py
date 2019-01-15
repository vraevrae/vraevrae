from models.Quiz import Quiz
from models.Question import Question
from models.User import User
from helpers.fake import apiQuestion


class App ():
    """the application itself, holds the stores and some lookup functions"""

    def __init__(self, **kwargs):
        self.quizes = {}
        self.questions = {}
        self.answers = {}
        self.users = {}

    def createQuiz(self):
        """creates a new quiz and adds it to the app"""
        newQuiz = Quiz()
        self.quizes[newQuiz.quizId] = newQuiz
        self.createQuestion(newQuiz.quizId)
        return newQuiz.quizId

    def getQuiz(self, quizId):
        """read a specific quiz from the app by quizId"""
        return self.quizes[quizId]

    def createQuestion(self, quizId):
        """create a new question and add it to the app and to the quiz"""
        newQuestion = Question(**apiQuestion())
        self.getQuiz(quizId).addQuestionById(newQuestion.questionId)
        self.questions[newQuestion.questionId] = newQuestion
        return newQuestion.questionId

    def getQuestion(self, questionId):
        """reads a specific question from the app by questionId"""
        return self.questions[questionId]

    def createUser(self, quizId, user):
        """adds a user to the app"""
        newUser = User(**user)
        self.users[newUser.userId] = newUser
        self.getQuiz(quizId).addUserById(newUser.userId)
        return newUser.userId

    def getUser(self, userId):
        """reads a specific user from the app  by userId"""
        return self.users[userId]
