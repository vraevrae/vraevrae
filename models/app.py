from models.quiz import Quiz
from models.question import Question
from models.user import User
from models.answer import Answer


class App ():
    """the application itself, owns the stores and some lookup functions"""

    def __init__(self):
        self.quizes = {}
        self.questions = {}
        self.answers = {}
        self.users = {}

    def create_quiz(self, Source):
        """creates a new quiz and adds it to the store"""
        code = 1
        if len(self.questions) is not 0:
            code = max([quiz.code for quiz in self.quizes.values()]) + 1

        new_quiz = Quiz(Source, code)
        self.quizes[new_quiz.quiz_id] = new_quiz
        return new_quiz.quiz_id

    def get_quiz_by_id(self, quiz_id):
        """read a specific quiz from the store by quizId"""
        return self.quizes[quiz_id]

    def create_question_from_source(self, quiz_id):
        """Creates a question with answers from a given source"""
        # get question from quiz source
        temp_question = self.get_quiz_by_id(quiz_id).source.get_question()

        # add the question to the store
        question_id = self.create_question(quiz_id, temp_question)

        # add the answers to the question and the store
        for answer in temp_question["answers"]:
            self.create_answer(
                question_id, answer["text"], answer["is_correct"])

        return question_id

    def create_question(self, quiz_id, temp_question):
        """create a new question and add it to the store and to the quiz"""

        new_question = Question(**temp_question)
        self.get_quiz_by_id(quiz_id).add_question_by_id(
            new_question.question_id)
        self.questions[new_question.question_id] = new_question
        return new_question.question_id

    def get_question_by_id(self, question_id):
        """reads a specific question from the store by questionId"""
        return self.questions[question_id]

    def create_answer(self, question_id, text, is_correct):
        """create a new question and add it to the store and to the quiz"""
        new_answers = Answer(question_id, text, is_correct)
        self.get_question_by_id(question_id).add_answer_by_id(
            new_answers.answer_id)
        self.answers[new_answers.answer_id] = new_answers
        return new_answers.answer_id

    def get_answer_by_id(self, answer_id):
        """reads a specific question from the store by questionId"""
        return self.answers[answer_id]

    def create_user(self, quiz_id, name, session_id, is_owner):
        """adds a user to the app"""
        new_user = User(quiz_id=quiz_id, name=name,
                        session_id=session_id, is_owner=is_owner)
        self.users[new_user.user_id] = new_user
        self.get_quiz_by_id(quiz_id).add_user_by_id(new_user.user_id)
        return new_user.user_id

    def get_user_by_id(self, user_id):
        """reads a specific user from the store by userId"""
        return self.users[user_id]

    def new_quiz(self, name, session_id, Source):
        """creates a default quiz"""
        quiz_id = self.create_quiz(Source)
        for _ in range(10):
            self.create_question_from_source(quiz_id)

        self.create_user(quiz_id=quiz_id, name=name,
                         session_id=session_id, is_owner=True)

        return quiz_id

    # def join_quiz(self, name, session_id, code):
    #     """joins a new user to a quiz"""
    #     self.create_user(quiz_id=quiz_id, name=name,
    #                      session_id=session_id, is_owner=False)

    #     return quiz_id
