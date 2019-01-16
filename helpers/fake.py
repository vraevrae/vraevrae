class FakeSource():

    def getQuestion(self):
        "Fake function that simulates an API call and returns a question with answers"
        return {"text": "a question",
                "answers": [
                    {"text": "",
                     "correct": True},
                    {"text": "",
                     "correct": True},
                    {"text": "",
                     "correct": True},
                    {"text": "",
                     "correct": True},
                ],
                "category": "finance",
                "difficulty": "hard"}
