class View():
    def __init__(self, user):
        self.type = "lobby"  # lobby / question / scoreboard
        self.data = {
            "question": "a question",
            "answsers": ["a list of answers"],
            "users": "a list of users",
            "user": "you, yourself"
        }
