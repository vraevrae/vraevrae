"""
Heavily edited: 

1. Uniqueness was not guaranteed: the same request was being send away and yielded a random response
   Two ways to deal with the indeterminism of OpenTDB: 
    - Keep all questions arround or start a session
    - I opted to write it with a session, less code and requests needed.
2. The buffer was overwritten on each request, instead of being a fifo queue in which stuff gets added on the end
3. There was quite a bit of premature optimisations. 
    - Try ... except statement hide a lot of errors making traces quite a bit harder.
    - The arrow type statements aren't enforced, and were actually incorrect
    - Also the entanglement with a config file seemed more annoying to me than beneficial. It really only makes 
      sense for things that should actually be configurable, else it's just another place to check
    - Making the buffer cache when at lower than x questions didnt make sense in synchrounous code, because it actually
      cause more delays than it solves (especially with categories and difficulties). 
      Ansynchronously, however, it would make sense. 
4. Inheritance is much nicer in this case than two seperate composed classes
    - I opted to rewrite to inheritance, this makes the use of "self" much more efficient and allows for
      polymorphism (although it's trivial here)
    - Also watch where you store variables in an OO design, some were on the class, not the instance,
      where that didn't make much sense. The source class would cache for ALL sources, which yields 
      trouble when testing, because you'd expect an new instantiation of a source to have an empty cache.
"""


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
