# def test_next_question():
#     app = App()

#     user_id = app.new_quiz("Creator", FakeSource)

#     old_quiz = app.store.get_quiz_by_user_id(user_id)
#     old_quiz.start()
#     old_quiz_current_question = old_quiz.current_question
#     sleep(1.1)
#     old_quiz.next_question()

#     new_quiz = app.store.get_quiz_by_user_id(user_id)

#     assert old_quiz_current_question is new_quiz.current_question - 1

# def test_next_question_causes_finish():
#     app = App()

#     user_id = app.new_quiz("Creator", FakeSource)

#     quiz = app.store.get_quiz_by_user_id(user_id)
#     quiz.start()
#     for _ in range(10):
#         sleep(1.1)
#         quiz.next_question()

#     new_quiz = app.store.get_quiz_by_user_id(user_id)

#     assert new_quiz.is_finished

# def test_finish_quiz():
#     app = App()

#     user_id = app.new_quiz("Creator", FakeSource)

#     quiz = app.store.get_quiz_by_user_id(user_id)

#     quiz.finish()

#     assert quiz.is_finished is True
#     # lcprint(vars(quiz), "the ended quest:")
