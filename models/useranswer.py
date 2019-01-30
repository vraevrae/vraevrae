from uuid import uuid4


class UserAnswer:
    """quiz user_answer, inherits from answer"""

    def __init__(self, question_id, answer_id, user_id):
        self.user_answer_id = str(uuid4())
        self.question_id = question_id
        self.answer_id = answer_id
        self.user_id = user_id
