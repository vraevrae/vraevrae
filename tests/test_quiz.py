from models.quiz import Quiz
from helpers.fake import FakeSource
from time import sleep
from helpers.cprint import lcprint
from config import MAX_TIME_IN_SECONDS


def test_next_question():
    Quiz.max_time_in_seconds = 0.1
    quiz = Quiz(FakeSource, 1234, "easy", "9")
    quiz.start()
    start_question = quiz.current_question

    sleep(0.1)
    quiz.next_question()
    second_question = quiz.current_question

    assert start_question is second_question - 1


def test_finish_quiz():
    quiz = Quiz(FakeSource, 1234, "easy", "9")
    quiz.finish()
    assert quiz.is_finished is True


def test_next_question_causes_finish():
    Quiz.max_time_in_seconds = 0.1
    quiz = Quiz(FakeSource, 1234, "easy", "9")
    quiz.start()

    for _ in range(10):
        sleep(0.1)
        quiz.next_question()

    assert quiz.is_finished
