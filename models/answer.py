from uuid import uuid4


class Answer:
    """an answer to a question, stored on the app for easy access"""

    def __init__(self, question_id, text, is_correct):
        self.answer_id = str(uuid4())
        self.question_id = question_id
        self.text = text
        self.is_correct = is_correct
