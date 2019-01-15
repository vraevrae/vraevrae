from uuid import uuid4


class Answer():
    """an answer to a question, stored on the app for easy access"""

    def __init__(self, questionId, text, isCorrect):
        self.answerId = str(uuid4())
        self.questionId = questionId
        self.text = text
        self.isCorrect = isCorrect

    def checkAnswer(self):
        """"checks the answer to the question"""
        # TODO
        pass
