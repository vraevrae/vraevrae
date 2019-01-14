import random
import pprint
pp = pprint.PrettyPrinter(depth=6)


def apiQuestion():
    return {"question": "a question",
            "answers": [
                "answer 1",
                "answer 2",
                "answer 3",
                "answer 4",
            ]
            }


class Quiz ():
    "Class that defines the quiz itself"

    def __init__(self):
        quizId = random.randrange(100000000)
        self.id = quizId
        self.questions = [Question(quizId) for question in range(10)]
        self.users = [User("somename")]

    isStarted = False
    activeQuestion = "34856389465"

    def addPlayer():
        return "TODO"

    def nextQuestion():
        return "TODO"

    def finished():
        return "TODO"


class Question():
    "Class that defines the questions of a quiz"

    def __init__(self, quizId):
        question = apiQuestion()

        self.id = random.randrange(100000000)
        self.question = question["question"]
        self.answers = question["answers"]
        self.timer = 10
        self.quizId = quizId


class User():
    "Class that defines the participants in a quiz"

    def __init__(self, name):
        self.id = random.randrange(100000000)
        self.name = name
        self.score = 1
        self.isOwner = False

    def updateScore():
        return "TODO"


pp.pprint(vars(Quiz()))
