class FakeSource():

    def getQuestion(self):
        "Fake function that simulates an API call and returns a question with answers"
        return {"text": "a question",
                "answers": [
                    {"text": "something 1",
                     "isCorrect": False},
                    {"text": "something 2",
                     "isCorrect": False},
                    {"text": "something 3",
                     "isCorrect": False},
                    {"text": "something 4",
                     "isCorrect": True},
                ],
                "category": "finance",
                "difficulty": "hard"}
