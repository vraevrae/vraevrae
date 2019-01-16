from models.store import Store


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
