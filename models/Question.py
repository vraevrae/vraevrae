from uuid import uuid1


def apiQuestion():
    "Function that calls the API for a new question"
    return {"question": "a question",
            "answers": [
                "answer 1",
                "answer 2",
                "answer 3",
                "answer 4",
            ]
            }


class Question():
    "Class that defines the questions of a quiz"

    def __init__(self, quizId):
        question = apiQuestion()

        self.quizId = quizId
        self.questionId = uuid1()
        self.question = question["question"]
        self.answers = question["answers"]
        self.timer = 10
