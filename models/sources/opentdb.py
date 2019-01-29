from random import shuffle

import requests

from models.source import Source
import config


class OpenTDB(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_amount_of_question(self):
        # print("get total count")
        query = f"https://opentdb.com/api_count.php?category=9"
        r = requests.get(query)
        json = r.json()
        # print(json)
        return 10

    def download_questions(self) -> dict:
        """
        Internal function to get apidata from Open Trivia DB
        :returns JSON data
        """
        # try to get a correct request from Open Trivia DB
        query = f"https://opentdb.com/api.php?amount={str(self.amount_of_questions)}&type=multiple"
        if self.difficulty:
            query += f"&difficulty={str(self.difficulty)}"
        if self.category:
            query += f"&category={str(self.category)}"

        try:
            print("send query: ", query)
            r = requests.get(query)
            json = r.json()

            # sucess: return data
            if json["response_code"] == 0:
                return json["results"]
            # not enough questions: raise exception
            elif json["response_code"] == 1:
                category_name = [category["name"] for category in config.CATEGORIES if int(
                    category["id"]) == int(self.category)][0]
                raise Exception(
                    f"[Datasource] category {category_name} with difficulty {str(self.difficulty)} does not have enough questions")
            # unknown error: raise exception
            else:
                raise Exception(
                    f"[Datasource] opentdb unknown error. Request URL: {query}")

        # raise an exception if there is an error with the request
        except requests.exceptions.RequestException as e:
            raise Exception(f"[Datasource] request has failed: {str(e)}")

    @staticmethod
    def format_question(unformatted_question) -> dict:
        """function to format data for use"""

        # shuffle answers to make sure the correct answer is not at the same place in the list
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

        shuffle(answers)

        # return dictonary
        return {"text": unformatted_question["question"],
                "answers": answers,
                "category": unformatted_question["category"],
                "difficulty": unformatted_question["difficulty"],
                "type": unformatted_question["type"]}
