from abc import ABC
from random import shuffle
from typing import List, Dict, Union

from models.source import Source


class Fixed(Source, ABC):
    """
    Open Trivia Database

    A trivia database with a free API licenced under Creative Commons
    Attribution-ShareAlike 4.0 International License.

    https://opentdb.com by PixelTail Games LCC
    """

    def __init__(self, *args, **kwargs):
        # call the parent class init to get caching and interface to the
        # rest of the models
        super().__init__(*args, **kwargs)

    @staticmethod
    def format_question() -> List[
        Dict[str, Union[str, List[Dict[str, Union[str, bool]]]]]]:
        q = [
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

        return q
