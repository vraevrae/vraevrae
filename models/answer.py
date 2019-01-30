from uuid import uuid4


class Answer:
    """
    an answer to a question, and its correctness

    not to be confused with a user_answer, which contains the users decisions
    concering the question. 
    """

    def __init__(self, question_id, text, is_correct):
        self.answer_id = str(uuid4())
        self.question_id = question_id
        self.text = text
        self.is_correct = is_correct
