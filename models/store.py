from models.answer import Answer
from models.question import Question
from models.quiz import Quiz
from models.user import User
from models.useranswer import UserAnswer


class Store:
    def __init__(self):
        self.quizes = {}
        self.questions = {}
        self.answers = {}
        self.users = {}
        self.user_answers = {}

    def create_quiz(self, source, difficulty=None):
        """creates a new quiz and adds it to the store"""
        # Get the lowest available code
        code = 1
        if len(self.questions) is not 0:
            code = max([quiz.code for quiz in self.quizes.values()]) + 1

        new_quiz = Quiz(source, code, difficulty)
        self.quizes[new_quiz.quiz_id] = new_quiz
        return new_quiz.quiz_id

    def create_answer(self, question_id, text, is_correct):
        """create a new answer and add it to the store and to the quiz"""
        new_answers = Answer(question_id, text, is_correct)
        self.get_question_by_id(question_id).add_answer_by_id(
            new_answers.answer_id)
        self.answers[new_answers.answer_id] = new_answers
        return new_answers.answer_id

    def create_user(self, quiz_id, name, is_owner):
        """adds a user to the app"""
        new_user = User(quiz_id=quiz_id, name=name, is_owner=is_owner)
        self.users[new_user.user_id] = new_user
        self.get_quiz_by_id(quiz_id).add_user_by_id(new_user.user_id)
        return new_user.user_id

    def create_question(self, quiz_id, temp_question):
        """create a new question and add it to the store and to the quiz"""
        new_question = Question(**temp_question)
        self.get_quiz_by_id(quiz_id).add_question_by_id(
            new_question.question_id)
        self.questions[new_question.question_id] = new_question
        return new_question.question_id

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

    def create_user_answer(self, user_id, answer_id):
        """Create user answer class which saves every answer the user has given"""

        try:
            answers = [answer for answer in self.user_answers if answer.question_id ==
                       self.answers[answer_id].question_id and answer.answer_id == answer_id]
        except AttributeError:
            answers = []

        if len(answers) == 0:
            new_user_answer = UserAnswer(user_id, self.get_quiz_by_user_id(user_id).quiz_id,
                                         answer_id)

            self.user_answers[new_user_answer.user_answer_id] = new_user_answer

            return new_user_answer
        else:
            return False

    def get_quiz_by_id(self, quiz_id):
        """read a specific quiz from the store by quizId"""
        return self.quizes[quiz_id]

    def get_quiz_by_code(self, code):
        """read a specific quiz from the store by quizId"""
        data = [quiz for quiz in self.quizes.values() if quiz.code is int(code)]
        if len(data) != 0:
            return data[0]

        return False

    def get_quiz_by_user_id(self, user_id):
        """reads a specific question from the store by questionId"""
        user = self.get_user_by_id(user_id)
        return self.get_quiz_by_id(user.quiz)

    def get_question_by_id(self, question_id):
        """reads a specific question from the store by questionId"""
        return self.questions[question_id]

    def get_answer_by_id(self, answer_id):
        """reads a specific question from the store by questionId"""
        return self.answers[answer_id]

    def get_answers_by_id(self, answer_ids):
        """reads a specific question from the store by questionId"""
        return [self.get_answer_by_id(answer_id) for answer_id in answer_ids]

    def get_user_by_id(self, user_id):
        """reads a specific user from the store by userId"""
        return self.users[user_id]

    def get_users_by_id(self, user_ids):
        """reads a list of users from the store by userId"""
        print("STORE USER:", self.users)
        return [self.get_user_by_id(user_id) for user_id in user_ids]


store = Store()
