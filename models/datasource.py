import config
from .sources import opentdb


class Datasource:
    """Class for getting and reformatting apidata from an external API"""

    # create variable for saving apidata between functions
    source = None
    cache_data = []
    current_question = 0

    def __init__(self, source=config.DEFAULT_DATASOURCE):
        # if source is not possible (not coded) raise an error
        if source not in config.POSSIBLE_DATASOURCES:
            raise NameError("[Datasource] source does not exist! Source: " + source.__str__())

        # print all given apidata for debug purposes if DEBUG is True
        print("[Datasource] source:", source) if config.DEBUG else None

        # define source
        if source == "opentdb":
            self.source = opentdb.OpenTDB()

        # save questions to cache_data
        self.update_cache_data()

    @staticmethod
    def get_datasources() -> list:
        """Return all possible datasources (as noted in config)"""
        return config.POSSIBLE_DATASOURCES

    def update_cache_data(self) -> None:
        """Save questions to cache_data"""
        self.cache_data = self.get_all_questions()

    def get_all_questions(self) -> list:
        """Function that returns all questions (formatted)"""
        return self.source.get_formatted_data()

    def get_question(self, current_question=current_question) -> dict:
        """Function that returns a question (that should not have been send in the current session)"""
        current_question = current_question % len(self.cache_data)
        self.current_question += 1

        if len(self.cache_data) - 5 == self.current_question:
            self.update_cache_data()

        return self.cache_data[current_question]
