class Source:
    """Class for getting, formatting and buffering data from an external API"""

    def __init__(self, difficulty=None, category=None):
        """create the cache, store configuration, and set a default available questions"""
        self.cached_questions = []
        self.difficulty = difficulty
        self.category = category
        self.available_questions_count = 10

    def get_question(self):
        """external interface to be used by the rest of the models"""
        return self.get_question_from_cache()

    def get_question_from_cache(self):
        """function that returns a question and initatiates a new request, if needed"""
        question = self.cached_questions[0]
        self.cached_questions.remove(question)

        # get new questions if the is empty and the api has questions available
        if len(self.cached_questions) == 0 and self.available_questions_count > 0:
            self.add_questions_to_cache()

        # raise error if the cache and API is empty
        if len(self.cached_questions) == 0 and self.available_questions_count == 0:
            raise Exception(
                "not enough questions available in this category / difficulty combination")

        return question

    def add_questions_to_cache(self):
        """save questions to cache_data"""
        questions = self.download_questions()
        self.cached_questions.extend(questions)

    def download_questions(self):
        """stub for child class"""
        raise NotImplementedError(
            "child class should implement specifics of authentication, downloading and formatting")
