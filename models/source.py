import config


"""
Heavily edited: 

1. Uniqueness was not guaranteed: the same request was being send away and yielded a random response
    - This indeterminism requires that all questions need to be maintained and checked
    - The buffer was overwritten on each request, instead of being a fifo queue
2. There were quite a bit of premature optimisations. 
    - Try ... except statement hide a lot of errors making traces quite a bit harder.
3. Inheritance or composition is much nicer than entanglement with a configuration file  
    - I opted to rewrite to inheritance, this makes the use of "self" much more efficient and allows for
      polymorphism.


"""


class Source:
    """Class for getting and reformatting apidata from an external API"""

    def __init__(self, difficulty=None, category=None, amount_of_questions=10):
        # create variable for saving apidata between functions
        self.cached_questions = []
        self.difficulty = difficulty
        self.category = category
        self.amount_of_questions = amount_of_questions

        # save questions to cache_data
        self.amount_of_questions = self.get_amount_of_question()
        self.add_questions_to_cache()

    def get_question(self) -> dict:
        """
        Function that returns a question
        (that should not have been send in the current session)
        """
        question = self.cached_questions[0]
        self.cached_questions.remove(question)

        if len(self.cached_questions) <= 5:
            self.add_questions_to_cache()

        return question

    def get_question_from_cache(self):
        pass

    def add_questions_to_cache(self) -> None:
        """Save questions to cache_data"""
        questions = self.get_questions_from_api()
        self.cached_questions.extend(questions)

    def get_questions_from_api(self) -> list:
        """function to return all formatted questions"""
        raw_questions = self.download_questions()
        return [self.format_question(raw_question) for raw_question in raw_questions]

    def get_amount_of_question(self):
        raise NotImplementedError("Parent class should not be instantiated")

    def download_questions(self) -> dict:
        raise NotImplementedError("Parent class should not be instantiated")

    @staticmethod
    def format_question(unformatted_question) -> dict:
        raise NotImplementedError("Parent class should not be instantiated")
