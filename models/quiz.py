import datetime
from uuid import uuid4

import config


class Quiz:
    """the central class of the application"""

    max_time_in_seconds = config.MAX_TIME_IN_SECONDS
    max_questions = config.MAX_QUESTIONS

    # Object attributes, different for each quiz
    def __init__(self, Source, code, difficulty, category, max_questions):
        if max_questions:
            self.max_questions = max_questions
        self.quiz_id = str(uuid4())
        self.code = code
        self.questions = []
        self.users = []
        self.is_started = False
        self.start_time = None
        self.is_finished = False
        self.current_question = 0
        self.difficulty = difficulty
        self.category = category
        self.source = Source(difficulty=difficulty, category=category)

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
        """returns a a boolean that indicates wether the quiz should update due to time"""
        next_update = self.max_time_in_seconds * (self.current_question + 1)
        update_time = self.start_time + datetime.timedelta(seconds=next_update)
        current_time = datetime.datetime.utcnow()
        return current_time > update_time

    def question_should_update_max_questions(self):
        """returns a a boolean that indicates wether the quiz should finish due to end of questions"""
        return self.current_question < self.max_questions - 1

    def next_question(self):
        """increments the quiz to to the next question"""
        if self.question_should_update_time():
            if self.question_should_update_max_questions():
                self.current_question += 1
            else:
                self.is_finished = True

        return self.current_question
