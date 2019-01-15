from uuid import uuid4


class User():
    """Quiz users"""

    def __init__(self, *args, **kwargs):
        self.userId = str(uuid4())
        self.name = kwargs["name"]
        self.score = 0
        self.isOwner = False

    def addScore(self):
        """Adds the score to the users score"""
        pass
