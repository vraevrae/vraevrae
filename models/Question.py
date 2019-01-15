from uuid import uuid4


class Question():
    """a questions is a fundamental stepping stone in a quiz"""

    def __init__(self, *args, **kwargs):
        self.questionId = str(uuid4())
        self.text = kwargs["text"]
        self.difficulty = kwargs["difficulty"]
        self.category = kwargs["category"]
        self.anwsers = []
        self.timer = 10

    def addAnswer(self):
        """"adds an answer to the quiz"""
        pass

    def checkAnswer(self):
        """"checks the answer to the question"""
        # TODO
        pass
