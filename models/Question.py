from uuid import uuid4


class Question():
    """"A quiz takes a user through many questions"""

    def __init__(self, quizId, question):
        self.quizId = quizId
        self.questionId = str(uuid4())
        self.question = question["question"]
        self.answers = question["answers"]
        self.timer = 10

    def checkAnswer(self):
        """"Checks the answer to the question"""
        # TODO
        pass
