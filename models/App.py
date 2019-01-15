from models.Quiz import Quiz
from models.User import User
from helpers.fake import apiQuestion


class App ():
    """The application itself, holds the stores and some lookup functions"""

    def __init__(self, **kwargs):
        self.quizes = {}
        self.questions = {}
        self.users = {}
        self.answers = {}

    def newQuiz(self):
        """Creates a new quiz and adds it to the app"""
        newQuiz = Quiz()
        newQuiz.addQuestion(**apiQuestion())
        newQuiz.addQuestion(**apiQuestion())
        self.quizes[newQuiz.quizId] = newQuiz

    def getQuiz(self, quizId):
        """gets a quiz from the app"""
        return self.quizes[quizId]

    def getQuizIds(self):
        """gets a quiz from the app"""
        return [quiz for quiz in self.quizes]

    def newUser(self, quizId, user):
        """adds a user to the app"""
        newUser = User(**user)
        self.users[newUser.userId] = newUser
        self.getQuiz(quizId).addUserById(newUser.userId)

    def getUser(self, userId):
        """Gets a specific user from the app"""
        return self.users[userId]

    def getUserIds(self):
        """Gets a list of userIds from the app"""
        return [user for user in self.users]
