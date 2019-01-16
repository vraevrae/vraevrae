from models.store import Store
from models.view import View


class App ():
    """the application itself, holds user interactions"""

    def __init__(self):
        self.store = Store()

    def new_quiz(self, name, session_id, Source):
        """creates a default quiz"""
        quiz_id = self.store.create_quiz(Source)
        for _ in range(10):
            self.store.create_question_from_source(quiz_id)

        self.store.create_user(quiz_id=quiz_id, name=name,
                               session_id=session_id, is_owner=True)

        return quiz_id

    def join_quiz(self, name, session_id, code):
        """joins a new user to a quiz"""
        quiz = self.store.get_quiz_by_code(code)
        self.store.create_user(quiz_id=quiz.quiz_id, name=name,
                               session_id=session_id, is_owner=False)

        return quiz

    def get_view(self, session_id):
        user = self.store.get_user_by_session_id(session_id)
        quiz = self.store.get_quiz_by_id(user.quiz)

        if not quiz.is_started:
            return View("lobby", {"users": self.store.get_users_by_id(quiz.users)})

        if quiz.is_started and not quiz.is_finished:
            question_id = quiz.get_current_question_id()
            question = self.store.get_question_by_id(question_id)
            answers = self.store.get_answers_by_id(question.answers)
            return View("question", {"question": question, "answers": answers})

        if quiz.is_finished:
            return View("scoreboard", {"users": self.store.get_users_by_id(quiz.users)})

    def start_quiz(self, session_id):
        user = self.store.get_user_by_session_id(session_id)

        if user.is_owner:
            return self.store.get_quiz_by_id(user.quiz).start()
