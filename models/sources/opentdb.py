from random import shuffle

import requests

from models.source import Source


class OpenTDB(Source):
    """
    Open Trivia Database

    A trivia database with a free API licenced under Creative Commons Attribution-ShareAlike 4.0 International License.

    https://opentdb.com by PixelTail Games LCC
    """

    def __init__(self, *args, **kwargs):
        # call the parent class init to get caching and interface to the rest of the models
        super().__init__(*args, **kwargs)

        # get session id and counts
        self.get_api_session_token()
        self.get_available_questions_count()

        # save first questions to cache_data
        self.add_questions_to_cache()

    def get_api_session_token(self) -> None:
        """set API session token to guarantee uniqueness"""
        query = "https://opentdb.com/api_token.php?command=request"
        json = requests.get(query).json()
        self.token = json["token"]

    def get_available_questions_count(self) -> None:
        """get the amount of questions for the current source configuration to avoid overfetching, and more importantly: errors"""
        # get counts of category
        if self.category:
            query = f"https://opentdb.com/api_count.php?category={self.category}"
            json = requests.get(query).json()
            counts = json["category_question_count"]

            # get the counts per difficulty
            if self.difficulty == "easy":
                self.available_questions_count = counts["total_easy_question_count"]
            elif self.difficulty == "medium":
                self.available_questions_count = counts["total_medium_question_count"]
            elif self.difficulty == "hard":
                self.available_questions_count = counts["total_hard_question_count"]
            else:
                self.available_questions_count = counts["total_question_count"]

        # get global counts if no category
        else:
            query = "https://opentdb.com/api_count_global.php"
            json = requests.get(query).json()
            self.available_questions_count = json["overall"]["total_num_of_questions"]

    def download_questions(self) -> list:
        """Internal function to get apidata from Open Trivia DB"""

        # check if API still has questions
        if self.available_questions_count < 1:
            raise Exception("API has run out of questions")

        # construct the query
        query = f"https://opentdb.com/api.php"

        query += f"?amount={str(self.available_questions_count)}"

        if self.category:
            query += f"&category={str(self.category)}"
        if self.difficulty:
            query += f"&difficulty={str(self.difficulty)}"
        if self.token:
            query += f"&token={str(self.token)}"

        # try to get questions from API
        try:
            r = requests.get(query)
            json = r.json()

            # sucess
            if json["response_code"] == 0:
                # reduce the remaining questions
                # TODO test this
                self.available_questions_count -= \
                    self.available_questions_count if \
                    self.available_questions_count < 50 else 50

                # format and return questions if of proper typ«e (all types
                # to to be downloaded because of limited API-count helper)
                return [self.format_question(raw_question) for raw_question
                        in json["results"] if raw_question["type"] ==
                        "multiple"]

            # unknown error
            else:
                raise Exception(
                    f"[Datasource] opentdb unknown error. Request URL:"
                    f" {query}")

        # error with the request
        except requests.exceptions.RequestException as e:
            raise Exception(f"[Datasource] request has failed: {str(e)}")

    @staticmethod
    def format_question(raw_question) -> List[Dict[str, Union[str, Any]]]:
        """function to format and shuffle the retrieved questions"""
        # format answers
        answers = [
            {"text": raw_question["incorrect_answers"][0],
                "is_correct": False},
            {"text": raw_question["incorrect_answers"][1],
                "is_correct": False},
            {"text": raw_question["incorrect_answers"][2],
                "is_correct": False},
            {"text": raw_question["correct_answer"],
                "is_correct": True},
        ]

        # shuffle answers to make sure the correct answer is not at the same place in the list
        shuffle(answers)
        return [
            {"text": "Welke wiskunde is nodig om informatiekunde te studeren?",
             "answers": shuffle([{"text": "Minimaal wiskunde B",
                                  "is_correct": False},
                                 {"text": "Dat maakt niet uit",
                                  "is_correct": False},
                                 {"text": "Dat maakt niet uit, maar wel met "
                                          "toelatingstest",
                                  "is_correct": False},
                                 {"text": "Minimaal wiskunde A",
                                  "is_correct": True}]),
             "category": "UvA",
             "difficulty": "easy",
             "type": "Presentation"},
            {"text": "Op welk beroep is de studie informatiekunde niet "
                     "gericht?",
             "answers": shuffle([{"text": "Data Scientist",
                                  "is_correct": False},
                                 {"text": "Interactieontwerper",
                                  "is_correct": False},
                                 {"text": "Onderzoeker",
                                  "is_correct": False},
                                 {"text": "Programmeur",
                                  "is_correct": True}]),
             "category": "UvA",
             "difficulty": "easy",
             "type": "Presentation"}
        ]
        # # return correctly formatted question
        # return {"text": raw_question["question"],
        #         "answers": answers,
        #         "category": raw_question["category"],
        #         "difficulty": raw_question["difficulty"],
        #         "type": raw_question["type"]}
