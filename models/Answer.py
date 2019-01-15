from uuid import uuid4


class Answer():
    """an answer fundamentally belongs to a question, but is stored normalized for easy access"""

    def __init__(self, **kwargs):
        self.answerId = str(uuid4())
        self.questionId = questionId
        self.text = text
        self.isCorrect = isCorrect

    def checkAnswer(self):
        """"checks the answer to the question"""
        # TODO
        pass
