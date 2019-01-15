from uuid import uuid4


class Question():
    """A quiz takes a user through many questions"""

    def __init__(self, text, difficulty, answers):
        self.questionId = str(uuid4())
        self.text = text
        self.difficulty = difficulty
        self.anwsers = []
        self.timer = 10

    def addAnswer(self):
        """"Adds an answer to the quiz"""
        pass

    def checkAnswer(self):
        """"Checks the answer to the question"""
        # TODO
        pass
