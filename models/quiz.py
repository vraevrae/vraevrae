from uuid import uuid4
from models.question import Question
from models.user import User
import datetime


class Quiz:
    """the central class of the application"""

    # Class attributes, should be the same for all quizes
    MAX_TIME_IN_SECONDS = 10
    MAX_QUESTIONS = 10

    # Object attributes, different for each quiz
    def __init__(self, Source, code):
        self.quiz_id = str(uuid4())
        self.code = code
        self.questions = []
        self.users = []
        self.is_started = False
        self.start_time = None
        self.is_finished = False
        self.current_question = 0
        self.source = Source()

    def add_question_by_id(self, question_id):
        """adds a question to the quiz"""
        self.questions = [*self.questions, question_id]

    def add_user_by_id(self, user_id):
        """adds a player to the quiz"""
        self.users = [*self.users, user_id]

    def start(self):
        """starts the quiz"""
        self.is_started = True
        self.start_time = datetime.datetime.utcnow()
        return self.quiz_id

    def get_current_question_id(self):
        """get the id of the current question"""
        return self.questions[self.current_question]

    def finish(self):
        """finishes the quiz"""
        self.is_finished = True
        return self.quiz_id

    def question_should_update_time(self):
        # print("TIMEDELTASTUFFF")

        should_update_at = self.MAX_TIME_IN_SECONDS * self.current_question
        current_time = datetime.datetime.utcnow()

        # print("should update at", should_update_at)
        # print("currente", current_time)
        # print("TIMEDELTASTUFFF-ENDEND", )
        return True

    def question_should_update_max_questions(self):
        return self.current_question < self.MAX_QUESTIONS - 1

    def next_question(self):
        """increments the quiz to to the next question"""
        if self.question_should_update_time():
            if self.question_should_update_max_questions():
                self.current_question += 1
            else:
                self.is_finished = True

        return self.current_question
