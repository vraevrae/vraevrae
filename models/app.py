from models.store import Store


class App (Store):
    """the application itself, owns the stores and some lookup functions"""

    def new_quiz(self, name, session_id):
        """creates a default quiz"""
        quiz_id = super().create_quiz(Source)
        for _ in range(10):
            super().create_question_from_source(quiz_id)

        super().create_user(quiz_id=quiz_id, name=name,
                            session_id=session_id, is_owner=True)

        return quiz_id

    def join_quiz(self, name, session_id, code):
        """joins a new user to a quiz"""
        quiz = super().get_quiz_by_code(code)
        super().create_user(quiz_id=quiz.quiz_id, name=name,
                            session_id=session_id, is_owner=False)

        return quiz
