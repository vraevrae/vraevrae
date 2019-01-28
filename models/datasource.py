import config
from .sources.opentdb import OpenTDB


class Datasource:
    """Class for getting and reformatting apidata from an external API"""

    # create variable for saving apidata between functions
    source = None
    difficulty = None
    cache_data = []

    def __init__(self, source=config.DEFAULT_DATASOURCE, difficulty=None):
        # if source is not possible (not coded) raise an error
        if source not in config.POSSIBLE_DATASOURCES:
            raise NameError("[Datasource] source does not exist! Source: " + source.__str__())

        # print all given apidata for debug purposes if DEBUG is True
        print("[Datasource] source:", source) if config.DEBUG else None

        # define source
        if source == "opentdb":
            self.source = OpenTDB()

        if difficulty is not None:
            self.difficulty = difficulty

        # save questions to cache_data
        self.update_cache_data()

    @staticmethod
    def get_datasources() -> list:
        """Return all possible datasources (as noted in config)"""
        return config.POSSIBLE_DATASOURCES

    def update_cache_data(self, difficulty=difficulty) -> None:
        """Save questions to cache_data"""
        self.cache_data = self.get_all_questions(difficulty)

    def get_all_questions(self, difficulty=difficulty) -> list:
        """Function that returns all questions (formatted)"""
        return self.source.get_formatted_data(difficulty)

    def get_question(self, difficulty=difficulty) -> dict:
        """
        Function that returns a question
        (that should not have been send in the current session)
        """
        question = self.cache_data[0]
        self.cache_data.remove(question)

        if len(self.cache_data) <= 20:
            self.update_cache_data(difficulty)

        return question
