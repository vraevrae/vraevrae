from models.app import App
from models.datasource import Datasource


def test_create_question_from_real_source():
    """questions can be added form a source"""
    app = App()
    quiz_id = app.store.create_quiz(Datasource)
    question_id = app.store.create_question_from_source(quiz_id)
    question = app.store.questions[question_id]
    assert question
