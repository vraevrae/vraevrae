from uuid import uuid4


class Question():
    """a questions is a fundamental stepping stone in a quiz"""

    def __init__(self, *args, **kwargs):
        self.questionId = str(uuid4())
        self.text = kwargs["text"]
        self.difficulty = kwargs["difficulty"]
        self.category = kwargs["category"]
        self.answers = []
        self.timer = 10

    def addAnswerById(self, answerId):
        """"adds an answer to the quiz"""
        self.answers = [*self.answers, answerId]

    def checkAnswer(self):
        """"checks the answer to the question"""
        # TODO
        pass
