from uuid import uuid4


class User():
    """quiz users"""

    def __init__(self, **kwargs):
        self.user_id = str(uuid4())
        self.quiz = kwargs["quiz_id"]
        self.name = kwargs["name"]
        self.score = 0
        self.is_owner = kwargs["is_owner"]
