from uuid import uuid4


class Question():
    "Defines the questions of a quiz"

    def __init__(self, quizId, question):
        self.quizId = quizId
        self.questionId = str(uuid4())
        self.question = question["question"]
        self.answers = question["answers"]
        self.timer = 10

    def checkAnswer():
        "Checks the answer to the question"
        print("TODO")
