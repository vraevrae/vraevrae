from random import shuffle

import requests

import config


class OpenTDB:
    source = "opentdb"

    def __init__(self, difficulty, category, amount_of_questions=config.DATASOURCE_PROPERTIES[source]["maxRequest"]):
        self.amount_of_questions = amount_of_questions
        self.difficulty = difficulty
        self.category = category
        print("init: ", difficulty)

    def _download_data(self, amount_of_questions=1) -> dict:
        """
        Internal function to get apidata from Open Trivia DB
        :returns JSON data
        """
        # try to get a correct request from Open Trivia DB
        query = f"https://opentdb.com/api.php?amount={str(amount_of_questions)}&type=multiple"
        if self.difficulty:
            query += f"&difficulty={str(self.difficulty)}"
        if self.category:
            query += f"&category={str(self.category)}"

        try:
            r = requests.get(query)
            json = r.json()

            # check if request was correct
            if json["response_code"] == 0:
                # return apidata
                return json["results"]
            if json["response_code"] == 1:
                # rais an exception if not enough questions
                category_name = [category["name"] for category in config.CATEGORIES if int(
                    category["id"]) == int(self.category)]
                raise Exception(
                    f"category {category_name[0]} with difficulty {str(self.difficulty)} does not have enough questions")
            else:
                # raise an exception if the request was not correct
                raise Exception("[Datasource] opentdb response_code is not 0, request incorrect."
                                " Request URL: " + query)

        # raise an exception if there is an error with the request
        except requests.exceptions.RequestException as e:
            print(e) if config.DEBUG is True else None
            raise Exception(
                "[Datasource] opentdb request has an error: " + e.__str__())

    @staticmethod
    def _format_opentdb_data(data) -> dict:
        """function to format data for use"""

        # shuffle answers to make sure the correct answer is not at the same place in the list
        answers = [
            {"text": data["incorrect_answers"][0],
             "is_correct": False},
            {"text": data["incorrect_answers"][1],
             "is_correct": False},
            {"text": data["incorrect_answers"][2],
             "is_correct": False},
            {"text": data["correct_answer"],
             "is_correct": True},
        ]

        shuffle(answers)

        # return dictonary
        return {"text": data["question"],
                "answers": answers,
                "category": data["category"],
                "difficulty": data["difficulty"],
                "type": data["type"]}

    def get_formatted_data(self) -> list:
        """function to return all formatted questions"""
        return [self._format_opentdb_data(question) for question in self._download_data(
            self.amount_of_questions)]
