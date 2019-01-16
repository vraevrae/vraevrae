import requests
import config
from random import shuffle


class Datasource:
    """Class for getting and reformatting apidata from an external API"""

    # create variable for saving apidata between functions
    apidata = None

    def __init__(self, source=config.DEFAULT_DATASOURCE):
        print(config.DEFAULT_DATASOURCE, source)
        # if source is not possible (not coded) raise an error
        if source not in config.POSSIBLE_DATASOURCES:
            raise NameError("[Datasource] source does not exist! Source: " + source.__str__())

        # print all given apidata for debug purposes
        print("[Datasource] source:", source) if config.DEBUG else None

        # get new apidata
        self.get_new_question(source)

    def get_new_question(self, source=config.DEFAULT_DATASOURCE):
        if source == "opentdb":
            self.apidata = self._opentdb()

    @staticmethod
    def _opentdb(amountofquestions=50):
        """Internal function to get apidata from Open Trivia DB"""

        # try to get a correct request from Open Trivia DB
        try:
            # do request to Open Trivia DB API and format to JSON
            r = requests.get("https://opentdb.com/api.php?amount=" + str(amountofquestions) + "&type=multiple")
            json = r.json()

            # check if request was correct
            if json["response_code"] == 0:
                # return apidata
                return json["results"]
            else:
                # raise an exception if the request was not correct
                raise Exception("[Datasource] opentdb response_code is not 0, request incorrect. Request URL: "
                                + "https://opentdb.com/api.php?amount=" + str(amountofquestions) + "&type=multiple")

        # raise an exception if there is an error with the request
        except requests.exceptions.RequestException as e:
            print(e) if config.DEBUG is True else None
            raise Exception("[Datasource] opentdb request has an error: " + e.__str__())

    @staticmethod
    def get_datasources() -> list:
        """Return all possible datasources (as noted in config)"""
        return config.POSSIBLE_DATASOURCES

    def get_raw_data(self) -> list:
        """Return raw apidata used in class"""
        print(self.apidata)
        return self.apidata

    def get_data(self, questionnumber=0):
        """function to format data for use"""
        answers = [
            {"answer": self.apidata[questionnumber]["incorrect_answers"][0],
             "correct": False},
            {"answer": self.apidata[questionnumber]["incorrect_answers"][1],
             "correct": False},
            {"answer": self.apidata[questionnumber]["incorrect_answers"][2],
             "correct": False},
            {"answer": self.apidata[questionnumber]["correct_answer"],
             "correct": True},
        ]

        return {"question": self.apidata[questionnumber]["question"],
                "answers": shuffle(answers),
                "category": self.apidata[questionnumber]["category"],
                "difficulty": self.apidata[questionnumber]["difficulty"],
                "type": self.apidata[questionnumber]["type"]}
