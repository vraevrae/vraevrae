def apiQuestions(numQuestions):
    "Fake function that simulates an API call"
    return [{"question": "a question",
             "answers": [
                 "answer 1",
                 "answer 2",
                 "answer 3",
                 "answer 4",
             ]} for question in range(numQuestions)]
