from uuid import uuid4
from models.question import Question
from models.user import User


class Quiz ():
    """the central class of the application"""

    # Class attributes, should be the same for all quizes
    max_time = 10

    # Object attributes, different for each quiz
    def __init__(self, Source, code):
        self.quiz_id = str(uuid4())
        self.code = code
        self.questions = []
        self.users = []
        self.is_started = False
        self.is_finished = False
        self.is_deleted = False
        self.current_question = 0
        self.current_time = 0
        self.source = Source()

    def add_question_by_id(self, question_id):
        """adds a question to the quiz"""
        self.questions = [*self.questions, question_id]

    def add_user_by_id(self, user_id):
        """adds a player to the quiz"""
        self.users = [*self.users, user_id]

    def start(self):
        self.is_started = True
        return self.quiz_id

    def get_current_question_id(self):
        return self.questions[self.current_question]

    def finish(self):
        self.is_finished = True
        return self.quiz_id

    def check_answer(self, question_id, user_id):
        """asks the question wether the answer is correct, and adds the score to the user"""
        # TODO
        pass

    def next_question(self):
        """increments the quiz to to the next question"""
        # TODO
        pass
