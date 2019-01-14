from uuid import uuid1


class User():
    "Class that defines the participants in a quiz"

    def __init__(self, name):
        self.userId = uuid1()
        self.name = name
        self.score = 1
        self.isOwner = False

    def updateScore():
        return "TODO"
