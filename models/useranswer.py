from uuid import uuid4


class UserAnswer:
    """quiz useranswer"""

    def __init__(self, user_id, quiz_id, answer_id):
        self.user_answer_id = str(uuid4())
        self.user_id = user_id
        self.answer_id = answer_id
        self.quiz_id = quiz_id
