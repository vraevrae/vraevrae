from models.quiz import Quiz
from models.question import Question
from models.user import User
from models.answer import Answer
from helpers.fake import apiQuestion


class App ():
    """the application itself, holds the stores and some lookup functions"""

    def __init__(self):
        self.quizes = {}
        self.questions = {}
        self.answers = {}
        self.users = {}

    def createQuiz(self):
        """creates a new quiz and adds it to the app"""
        newQuiz = Quiz()
        self.quizes[newQuiz.quizId] = newQuiz
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

    def createAnswer(self, questionId, text, isCorrect):
        """create a new question and add it to the app and to the quiz"""
        newAnswers = Answer(questionId, text, isCorrect)
        self.getQuestion(questionId).addAnswerById(newAnswers.answerId)
        self.answers[newAnswers.answerId] = newAnswers
        return newAnswers.answerId

    def getAnswer(self, answerId):
        """reads a specific question from the app by questionId"""
        return self.answers[answerId]

    def createUser(self, quizId, name, sessionId):
        """adds a user to the app"""
        newUser = User(quizId=quizId, name=name, sessionId=sessionId)
        self.users[newUser.userId] = newUser
        self.getQuiz(quizId).addUserById(newUser.userId)
        return newUser.userId

    def getUser(self, userId):
        """reads a specific user from the app  by userId"""
        return self.users[userId]

    def newQuiz(self, name, sessionId):
        """creates a full new quiz"""
        quizId = self.createQuiz()
        userId = self.createUser(quizId=quizId, name=name, sessionId=sessionId)
