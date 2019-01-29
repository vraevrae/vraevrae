from models.source import Source
from models.store import Store


def test_create_question_from_real_source():
    """questions can be added form a source"""
    store = Store()
    quiz_id = store.create_quiz(Source)
    question_id = store.create_question_from_source(quiz_id)
    question = store.questions[question_id]
    assert question


def test_create_question_from_real_source_without():
    """questions can be added form a source"""
    store = Store()
    quiz_id = store.create_quiz(Source, difficulty=None, category=None)
    question_id = store.create_question_from_source(quiz_id)
    question = store.questions[question_id]
    assert question


def test_create_question_from_real_source_with_category():
    """questions can be added form a source"""
    store = Store()
    quiz_id = store.create_quiz(Source, difficulty=None, category=18)
    question_id = store.create_question_from_source(quiz_id)
    question = store.questions[question_id]
    assert question


def test_create_question_from_real_source_with_category_easy():
    """questions can be added form a source"""
    store = Store()
    quiz_id = store.create_quiz(Source, difficulty="easy", category=18)
    question_id = store.create_question_from_source(quiz_id)
    question = store.questions[question_id]
    assert question


def test_create_question_from_real_source_with_category_medium():
    """questions can be added form a source"""
    store = Store()
    quiz_id = store.create_quiz(Source, difficulty="medium", category=18)
    question_id = store.create_question_from_source(quiz_id)
    question = store.questions[question_id]
    assert question


def test_create_question_from_real_source_with_category_hard():
    """questions can be added form a source"""
    store = Store()
    quiz_id = store.create_quiz(Source, difficulty="hard", category=18)
    question_id = store.create_question_from_source(quiz_id)
    question = store.questions[question_id]
    assert question
