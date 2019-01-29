from models.source import Source
from models.store import Store


def test_create_question_from_real_source():
    """questions can be added form a source"""
    store = Store()
    quiz_id = store.create_quiz(Source)
    question_id = store.create_question_from_source(quiz_id)
    question = store.questions[question_id]
    assert question
