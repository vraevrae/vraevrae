from flask import Flask, session
from flask_restful import Resource, Api, abort
from helpers import helpers
from models.datasource import Datasource
from models.store import Store

store = Store()


class Quiz(Resource):
    class New:
        def post(self, username, amount_of_questions=10):
            if username == "":
                abort(400)

            quiz_id = store.create_quiz(Datasource)
            for _ in range(amount_of_questions):
                store.create_question_from_source(quiz_id)

            user_id = store.create_user(quiz_id=quiz_id, name=username, is_owner=True)
            session["user_id"] = user_id

            return helpers.json_response({"quiz_id":quiz_id, "questions":store.questions})



    def get(self, user_id, quiz_id, question_id):

        # user = store.get_user_by_id(session["user_id"])
        # quiz = store.get_quiz_by_id(user.quiz)
        #
        # quiz.next_question()
        # question_id = quiz.get_current_question_id()
        # question = store.get_question_by_id(question_id)
        # answers = store.get_answers_by_id(question.answers)
        #
        # return helpers.json_response({"question":question, "answers":answers})