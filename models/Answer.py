from uuid import uuid4


class Answer():
    """A quiz takes a user through many questions"""

    def __init__(self, questionId, text, isCorrect):
        self.answerId = str(uuid4())
        self.questionId = questionId
        self.text = text
        self.isCorrect = isCorrect

    def checkAnswer(self):
        """"Checks the answer to the question"""
        # TODO
        pass
