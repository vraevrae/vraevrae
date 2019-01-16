from random import shuffle

import requests

import config


class OpenTDB:
    source = "opentdb"
    amount_of_questions = 0

    def __init__(self, amount_of_questions=config.DATASOURCE_PROPERTIES[source]["maxRequest"]):
        self.amount_of_questions = amount_of_questions

    @staticmethod
    def _download_data(amount_of_questions=1) -> dict:
        """
        Internal function to get apidata from Open Trivia DB
        :returns
        """

        # try to get a correct request from Open Trivia DB
        try:
            # do request to Open Trivia DB API and format to JSON
            r = requests.get("https://opentdb.com/api.php?amount=" + str(amount_of_questions) + "&type=multiple")
            json = r.json()

            # check if request was correct
            if json["response_code"] == 0:
                # return apidata
                return json["results"]
            else:
                # raise an exception if the request was not correct
                raise Exception("[Datasource] opentdb response_code is not 0, request incorrect. Request URL: "
                                + "https://opentdb.com/api.php?amount=" + str(amount_of_questions) + "&type=multiple")

        # raise an exception if there is an error with the request
        except requests.exceptions.RequestException as e:
            print(e) if config.DEBUG is True else None
            raise Exception("[Datasource] opentdb request has an error: " + e.__str__())

    @staticmethod
    def _format_opentdb_data(data) -> dict:
        """function to format data for use"""

        # shuffle answers to make sure the correct answer is not at the same place in the list
        answers = [
            {"answer": data["incorrect_answers"][0],
             "correct": False},
            {"answer": data["incorrect_answers"][1],
             "correct": False},
            {"answer": data["incorrect_answers"][2],
             "correct": False},
            {"answer": data["correct_answer"],
             "correct": True},
        ]

        # return dictonary
        return {"question": data["question"],
                "answers": shuffle(answers),
                "category": data["category"],
                "difficulty": data["difficulty"],
                "type": data["type"]}

    def get_formatted_data(self, amount_of_questions=amount_of_questions) -> list:
        """function to return all formatted questions"""
        return [self._format_opentdb_data(question) for question in self._download_data(amount_of_questions)]
