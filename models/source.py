import config


"""
Heavily edited: 

1. Uniqueness was not guaranteed: the same request was being send away and yielded a random response
    - Two ways to deal with the indeterminism of OpenTDB: Keep all questions arround or start a session
      I opted to write it with a session, less code and requests needed.
2. The buffer was overwritten on each request, instead of being a fifo queue
3. There was quite a bit of premature optimisations. 
    - Try ... except statement hide a lot of errors making traces quite a bit harder.
    - The arrow type statements aren't enforced, and were actually incorrect
4. Inheritance or composition is much nicer in this case than two seperate classes
    - I opted to rewrite to inheritance, this makes the use of "self" much more efficient and allows for
      polymorphism.
    - Also watch where you store variables in an OO design, some were on the class, not the instance,
      where that didn't make much sense. The source class would cache for ALL sources, which again yields 
      trouble when testing, because you'd expect an new instantion of a source to have an empty cache.
5. Also the entanglement with a config file seemed more annoying to me than beneficial. 
    - It really only makes sense for things that should actually be configurable, else it's just 
      another place to check
"""


class Source:
    """Class for getting, formatting and buffering data from an external API"""

    def __init__(self, difficulty=None, category=None):
        # create variable for saving apidata between functions
        self.cached_questions = []
        self.difficulty = difficulty
        self.category = category

    def get_question(self):
        """Function that returns a question and initatiates a new request, if needed"""
        question = self.cached_questions[0]
        self.cached_questions.remove(question)

        # TODO rewrite to take amount of questions under consideration
        if len(self.cached_questions) <= 5:
            self.add_questions_to_cache()

        return question

    def add_questions_to_cache(self):
        """Save questions to cache_data"""
        questions = self.download_questions()
        self.cached_questions.extend(questions)

    def download_questions(self):
        raise NotImplementedError(
            "Child class should implement specifics of authentication, downloading and formatting")
