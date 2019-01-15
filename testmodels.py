from models.App import App
from helpers.cprint import cprint
from helpers.fake import apiQuestion

# initialize the app
app = App()
print("An initialized app:")
cprint(vars(app))

# add a quiz to the app
app.createQuiz()
print("An app with an quiz:")
cprint(vars(app))

# get a quiz
firstQuizId = list(app.quizes.values())[0].quizId
print("A quiz:")
cprint(vars(app.getQuiz(firstQuizId)))

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
