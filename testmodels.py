from models.App import App
from helpers.cprint import cprint
from helpers.fake import apiQuestion

# initialize the app
app = App()
print("An initialized app:")
cprint(vars(app))

# add a quiz to the app
app.newQuiz()
print("An app with an quiz:")
cprint(vars(app))

# Get a quiz
firstQuiz = app.getQuizIds()[0]
print("A quiz:")
cprint(vars(app.getQuiz(firstQuiz)))

# add a user to the first quiz
app.newUser(firstQuiz, {"name": "Someone"})
print("A quiz with a user:")
cprint(vars(app.getQuiz(firstQuiz)))

# Get a user
firstUser = app.getUserIds()[0]
print("A user:")
cprint(vars(app.getUser(firstUser)))

# print out with colors the things inside the app
print("The final appstate:")
cprint(vars(app))
