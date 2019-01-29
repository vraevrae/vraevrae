# from models.store import Store
# from random import randint
# from helpers.cprint import cprint, lcprint
# from helpers.fake import FakeSource
# import pytest


# def test_create_quiz():
#     """quizes can be created"""
#     store = Store()
#     quiz_id = store.create_quiz(FakeSource)
#     assert store.quizes[quiz_id]


# def test_get_quiz():
#     """quizes can be retrieved from the app"""
#     store = Store()
#     quiz_id = store.create_quiz(FakeSource)
#     quiz = store.get_quiz_by_id(quiz_id)
#     assert quiz


# def test_create_question():
#     """questions can be added to a app and quiz"""
#     store = Store()
#     quiz_id = store.create_quiz(FakeSource)
#     question_id = store.create_question(
#         quiz_id, {"text": "some question", "difficulty": "medium", "category": "some category"})
#     question = store.questions[question_id]
#     assert question


# def test_create_question_from_fake_source():
#     """questions can be added form a source"""
#     store = Store()
#     quiz_id = store.create_quiz(FakeSource)
#     question_id = store.create_question_from_source(quiz_id)
#     question = store.questions[question_id]
#     assert question


# def test_get_question():
#     """questions can be retrieved from the app"""
#     store = Store()
#     quiz_id = store.create_quiz(FakeSource)
#     question_id = store.create_question_from_source(quiz_id)
#     question = store.get_question_by_id(question_id)
#     assert question


# def test_create_answer():
#     """answers can be added to a app and quiz"""
#     store = Store()
#     quiz_id = store.create_quiz(FakeSource)
#     question_id = store.create_question_from_source(quiz_id)
#     answer_id = store.create_answer(question_id, "some answer text", True)
#     answer = store.answers[answer_id]
#     assert answer


# def test_get_answer_by_id():
#     """answers can be retrieved from the app"""
#     store = Store()
#     quiz_id = store.create_quiz(FakeSource)
#     question_id = store.create_question_from_source(quiz_id)
#     answer_id = store.create_answer(question_id, "some answer text", True)
#     answer = store.get_answer_by_id(answer_id)
#     assert answer


# def test_get_answers_by_id():
#     """answers can be retrieved from the app"""
#     store = Store()
#     quiz_id = store.create_quiz(FakeSource)
#     question_id = store.create_question_from_source(quiz_id)
#     answer_id_one = store.create_answer(
#         question_id, "some answer text", True)
#     answer_id_two = store.create_answer(
#         question_id, "some answer text", False)
#     answers = store.get_answers_by_id([answer_id_one, answer_id_two])
#     assert type(answers) is list


# def test_create_user():
#     """a user can be added to the store and quiz"""
#     store = Store()
#     quiz_id = store.create_quiz(FakeSource)
#     user_id = store.create_user(quiz_id, "Someone", False)
#     user = store.users[user_id]
#     assert user


# def test_get_user_by_id():
#     """a user can be retrieved from the app"""
#     store = Store()
#     quiz_id = store.create_quiz(FakeSource)
#     user_id = store.create_user(quiz_id, "Someone", False)
#     user = store.get_user_by_id(user_id)
#     assert user


# def test_get_users_by_id():
#     """answers can be retrieved from the app"""
#     store = Store()
#     quiz_id = store.create_quiz(FakeSource)
#     user_id_one = store.create_user(quiz_id, "Someone", False)
#     user_id_two = store.create_user(quiz_id, "Someone", False)

#     users = store.get_users_by_id([user_id_one, user_id_two])
#     assert type(users) is list


# @pytest.fixture
# def filled_store():
#     """Creates a somewhat larger app to test that no extra things are added"""
#     store = Store()

#     quiz_count = 0
#     question_count = 0
#     user_count = 0

#     for _ in range(3):
#         quiz_id = store.create_quiz(FakeSource)
#         quiz_count += 1

#         for _ in range(5):
#             store.create_question_from_source(quiz_id)
#             question_count += 1

#         for _ in range(8):
#             store.create_user(quiz_id, "Someone", False)
#             user_count += 1

#     return store


# def test_filled_app(filled_store):
#     assert len(filled_store.quizes) == 3
#     assert len(filled_store.questions) == 3 * 5
#     assert len(filled_store.users) == 3 * 8


# def test_quiz_codes_uniqueness(filled_store):
#     """tests if each quiz has an unique human readable code"""
#     quiz_codes = [quiz.code for quiz in filled_store.quizes.values()]
#     assert len(quiz_codes) is len(set(quiz_codes))


# def test_get_quiz_by_code(filled_store):
#     """tests if a specific quiz can be found by code"""
#     quiz_code = list(filled_store.quizes.values())[0].code
#     quiz_by_code = filled_store.get_quiz_by_code(quiz_code)
#     assert quiz_by_code
