# TODO FIX FILE, ALL COMMENTED BECAUSE MODELS/APP IS DELETED
# from helpers.fake import FakeSource
# from helpers.cprint import cprint, lcprint
# from random import randint
# from models.store import Store
#
# def test_create_quiz():
#     """quizes can be created"""
#     quiz_id = Store.create_quiz(FakeSource)
#     assert Store.quizes[quiz_id]
#
#     # lcprint(vars(app), "an app with an quiz:")
#
#
# def test_get_quiz():
#     """quizes can be retrieved from the app"""
#     quiz_id = Store.create_quiz(FakeSource)
#     quiz = app.store.get_quiz_by_id(quiz_id)
#     assert quiz
#
#     # lcprint(vars(quiz), "a quiz:")
#
#
# def test_create_question():
#     """questions can be added to a app and quiz"""
#     app = App()
#     quiz_id = app.store.create_quiz(FakeSource)
#     question_id = app.store.create_question(
#         quiz_id, {"text": "some question", "difficulty": "medium", "category": "some category"})
#     question = app.store.questions[question_id]
#     assert question
#
#     # lcprint(vars(question), "a question:")
#
#
# def test_create_question_from_source():
#     """questions can be added form a source"""
#     app = App()
#     quiz_id = app.store.create_quiz(FakeSource)
#     question_id = app.store.create_question_from_source(quiz_id)
#     question = app.store.questions[question_id]
#     assert question
#
#     # lcprint(vars(question), "a question:")
#
#
# def test_get_question():
#     """questions can be retrieved from the app"""
#     app = App()
#     quiz_id = app.store.create_quiz(FakeSource)
#     question_id = app.store.create_question_from_source(quiz_id)
#     question = app.store.get_question_by_id(question_id)
#     assert question
#
#     # lcprint(vars(question), "a question:")
#
#
# def test_create_answer():
#     """answers can be added to a app and quiz"""
#     app = App()
#     quiz_id = app.store.create_quiz(FakeSource)
#     question_id = app.store.create_question_from_source(quiz_id)
#     answer_id = app.store.create_answer(question_id, "some answer text", True)
#     answer = app.store.answers[answer_id]
#     assert answer
#
#     # lcprint(vars(answer), "a answer:")
#
#
# def test_get_answer_by_id():
#     """answers can be retrieved from the app"""
#     app = App()
#     quiz_id = app.store.create_quiz(FakeSource)
#     question_id = app.store.create_question_from_source(quiz_id)
#     answer_id = app.store.create_answer(question_id, "some answer text", True)
#     answer = app.store.get_answer_by_id(answer_id)
#     assert answer
#
#     # lcprint(vars(answer), "a answer:")
#
#
# def test_get_answers_by_id():
#     """answers can be retrieved from the app"""
#     app = App()
#     quiz_id = app.store.create_quiz(FakeSource)
#     question_id = app.store.create_question_from_source(quiz_id)
#     answer_id_one = app.store.create_answer(
#         question_id, "some answer text", True)
#     answer_id_two = app.store.create_answer(
#         question_id, "some answer text", False)
#     answers = app.store.get_answers_by_id([answer_id_one, answer_id_two])
#     assert type(answers) is list
#
#     # lcprint(answers, "a answer:")
#
#
# def test_create_user():
#     """a user can be added to the store and quiz"""
#     app = App()
#     quiz_id = app.store.create_quiz(FakeSource)
#     user_id = app.store.create_user(quiz_id, "Someone", False)
#     user = app.store.users[user_id]
#     assert user
#
#     # lcprint(vars(user), "a user:")
#
#
# def test_get_user_by_id():
#     """a user can be retrieved from the app"""
#     app = App()
#     quiz_id = app.store.create_quiz(FakeSource)
#     user_id = app.store.create_user(quiz_id, "Someone", False)
#     user = app.store.get_user_by_id(user_id)
#     assert user
#
#     # lcprint(vars(user), "a user:")
#
#
# def test_get_users_by_id():
#     """answers can be retrieved from the app"""
#     app = App()
#     quiz_id = app.store.create_quiz(FakeSource)
#     user_id_one = app.store.create_user(quiz_id, "Someone", False)
#     user_id_two = app.store.create_user(quiz_id, "Someone", False)
#
#     users = app.store.get_users_by_id([user_id_one, user_id_two])
#     assert type(users) is list
#
#     # lcprint(users, "a list of users:")
#
#
# def test_filled_app():
#     """Creates a somewhat larger app to test that no extra things are added"""
#     app = App()
#
#     quiz_count = 0
#     question_count = 0
#     user_count = 0
#
#     for _ in range(randint(1, 3)):
#         quiz_id = app.store.create_quiz(FakeSource)
#         quiz_count += 1
#
#         for _ in range(randint(1, 10)):
#             app.store.create_question_from_source(quiz_id)
#             question_count += 1
#
#         for _ in range(randint(1, 10)):
#             app.store.create_user(quiz_id, "Someone", False)
#             user_count += 1
#
#     assert len(app.store.quizes) == quiz_count
#     assert len(app.store.questions) == question_count
#     assert len(app.store.users) == user_count
#
#     # lcprint(vars(app), "a filled app:")
#
#
# def test_quiz_codes_uniqueness():
#     """tests if each quiz has an unique human readable code"""
#     app = App()
#     app.new_quiz("some name", FakeSource)
#     app.new_quiz("some name", FakeSource)
#     app.new_quiz("some name", FakeSource)
#     app.new_quiz("some name", FakeSource)
#     app.new_quiz("some name", FakeSource)
#     quiz_codes = [quiz.code for quiz in app.store.quizes.values()]
#
#     assert len(quiz_codes) is len(set(quiz_codes))
#
#     # lcprint(quiz_codes, "the quiz codes:")
#
#
# def test_get_quiz_by_code():
#     """tests if a specific quiz can be found by code"""
#     app = App()
#     user_id = app.new_quiz("some name", FakeSource)
#     quiz = app.store.get_quiz_by_user_id(user_id)
#     quiz_by_code = app.store.get_quiz_by_code(quiz.code)
#
#     assert quiz_by_code
#
#     # lcprint(vars(quiz_by_code), "the quiz by code:")
