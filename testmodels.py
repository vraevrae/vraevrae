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

# Get a quiz
firstQuiz = app.readQuizIds()[0]
print("A quiz:")
cprint(vars(app.readQuiz(firstQuiz)))

# add a user to the first quiz
app.createUser(firstQuiz, {"name": "Someone"})
print("A quiz with a user:")
cprint(vars(app.readQuiz(firstQuiz)))

# Get a user
firstUser = app.readUserIds()[0]
print("A user:")
cprint(vars(app.readUser(firstUser)))

# print out with colors the things inside the app
print("The final appstate:")
cprint(vars(app))
