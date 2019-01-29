from random import shuffle
from urllib.parse import urlencode

import requests

from models.source import Source
import config

from helpers.cprint import lcprint


class OpenTDB(Source):
    def __init__(self, *args, **kwargs):
        # call the parent class init to get caching and external interface
        super().__init__(*args, **kwargs)

        # get session id
        self.get_api_session_token()

        # get category counts
        self.get_amount_of_questions()

        # save first questions to cache_data
        self.add_questions_to_cache()

    def get_api_session_token(self) -> None:
        """set API session token to guarantee uniqueness"""
        query = f"https://opentdb.com/api_token.php?command=request"
        json = requests.get(query).json()
        self.token = json["token"]

    def get_amount_of_questions(self) -> None:
        """get the amount of questions for the current source configuration to avoid overfetching, and more importantly: errors"""
        if self.category:
            query = f"https://opentdb.com/api_count.php?category={self.category}"
            json = requests.get(query).json()
            counts = json["category_question_count"]
            if self.difficulty == "easy":
                self.amount_of_questions = counts["total_easy_question_count"]
            elif self.difficulty == "medium":
                self.amount_of_questions = counts["total_medium_question_count"]
            elif self.difficulty == "hard":
                self.amount_of_questions = counts["total_hard_question_count"]
            else:
                self.amount_of_questions = counts["total_question_count"]
        else:
            query = "https://opentdb.com/api_count_global.php"
            json = requests.get(query).json()
            self.amount_of_questions = json["overall"]["total_num_of_questions"]

    def download_questions(self) -> list:
        """Internal function to get apidata from Open Trivia DB"""

        # check if API still has questions
        if self.amount_of_questions < 1:
            raise Exception("API has run out of questions")

        # construct the query
        query = f"https://opentdb.com/api.php"

        query += f"?amount={str(self.amount_of_questions)}"

        if self.category:
            query += f"&category={str(self.category)}"
        if self.difficulty:
            query += f"&difficulty={str(self.difficulty)}"
        if self.token:
            query += f"&token={str(self.token)}"

        # try to get questions from Open Trivia DB
        try:
            r = requests.get(query)
            json = r.json()

            # sucess
            if json["response_code"] == 0:
                # reduce the remaining questions
                self.amount_of_questions -= self.amount_of_questions if self.amount_of_questions < 50 else 50

                # format and return data
                return [self.format_question(raw_question) for raw_question in json["results"] if raw_question["type"] == "multiple"]

            # not enough questions
            elif json["response_code"] == 1:
                category_name = [category["name"] for category in config.CATEGORIES if int(
                    category["id"]) == int(self.category)][0]
                raise Exception(
                    f"[Datasource] category {category_name} with difficulty {str(self.difficulty)} does not have enough questions")

            # unknown error
            else:
                raise Exception(
                    f"[Datasource] opentdb unknown error. Request URL: {query}")

        # error with the request
        except requests.exceptions.RequestException as e:
            raise Exception(f"[Datasource] request has failed: {str(e)}")

    @staticmethod
    def format_question(unformatted_question) -> dict:
        """function to format and shuffle the retrieved questions"""
        # format answers
        answers = [
            {"text": unformatted_question["incorrect_answers"][0],
                "is_correct": False},
            {"text": unformatted_question["incorrect_answers"][1],
                "is_correct": False},
            {"text": unformatted_question["incorrect_answers"][2],
                "is_correct": False},
            {"text": unformatted_question["correct_answer"],
                "is_correct": True},
        ]

        # shuffle answers to make sure the correct answer is not at the same place in the list
        shuffle(answers)

        # return correctly formatted question
        return {"text": unformatted_question["question"],
                "answers": answers,
                "category": unformatted_question["category"],
                "difficulty": unformatted_question["difficulty"],
                "type": unformatted_question["type"]}
