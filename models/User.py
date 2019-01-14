from uuid import uuid4


class User():
    "Defines the participants in a quiz"

    def __init__(self, name):
        self.userId = str(uuid4())
        self.name = name
        self.score = 1
        self.isOwner = False

    def addScore(self):
        "Adds the score to the users score"
        return "TODO"
