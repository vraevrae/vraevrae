from models.Quiz import Quiz


class App ():
    """The application itself, holds the stores and some lookup functions"""

    def __init__(self, **kwargs):
        self.quizes = {}
        self.questions = {}
        self.users = {}
        self.answers = {}

    def newQuiz(self):
        newQuiz = Quiz()
        self.quizes[newQuiz.quizId] = newQuiz

    def getQuiz(self, quizId):
        return self.quizes[quizId]
