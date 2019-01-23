from uuid import uuid4
from config import DEFAULT_SCORE


class Question:
    """a questions is a fundamental stepping stone in a quiz"""

    def __init__(self, **kwargs):
        self.question_id = str(uuid4())
        self.text = kwargs["text"]
        self.difficulty = kwargs["difficulty"]
        self.category = kwargs["category"]
        self.answers = []
        self.score = DEFAULT_SCORE

    def add_answer_by_id(self, answer_id):
        """"adds an answer to the quiz"""
        self.answers = [*self.answers, answer_id]
