class View():
    def __init__(self, view_type, data):
        self.type = view_type  # lobby / question / scoreboard
        self.data = {
            "question": "a question",
            "answsers": ["a list of answers"],
            "users": "a list of users",
            "user": "you, yourself"
        }
