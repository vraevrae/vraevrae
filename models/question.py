from uuid import uuid4


class Question:
    """a questions is a fundamental stepping stone in a quiz"""

    def __init__(self, *args, **kwargs):
        self.question_id = str(uuid4())
        self.text = kwargs["text"]
        self.difficulty = kwargs["difficulty"]
        self.category = kwargs["category"]
        self.answers = []
        self.score = 10

    def add_answer_by_id(self, answer_id):
        """"adds an answer to the quiz"""
        self.answers = [*self.answers, answer_id]

    def check_answer(self):
        """"checks the answer to the question"""
        # TODO
        pass
