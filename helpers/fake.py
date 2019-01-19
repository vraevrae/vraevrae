class FakeSource:

    @staticmethod
    def get_question():
        """Fake function that simulates an API call and returns a question with answers"""
        return {"text": "a question",
                "answers": [
                    {"text": "something 1",
                     "is_correct": False},
                    {"text": "something 2",
                     "is_correct": False},
                    {"text": "something 3",
                     "is_correct": False},
                    {"text": "something 4",
                     "is_correct": True},
                ],
                "category": "finance",
                "difficulty": "hard"}
