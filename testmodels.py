from models.App import App


# initialize the app


# add a quiz to the app


# get a quiz


# get a question
firstQuestionId = list(app.questions.values())[0].questionId
print("A question:")
cprint(vars(app.getQuestion(firstQuestionId)))

# add a user to the first quiz
app.createUser(firstQuizId, {"name": "Someone"})
print("A quiz with a user:")
cprint(vars(app.getQuiz(firstQuizId)))

# get a user
firstUserId = list(app.users.values())[0].userId
print("A user:")
cprint(vars(app.getUser(firstUserId)))

# print out with colors the things inside the app
print("The final appstate:")
cprint(vars(app))
