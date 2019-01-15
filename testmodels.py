from models.App import App


# get a user
firstUserId = list(app.users.values())[0].userId
print("A user:")
cprint(vars(app.getUser(firstUserId)))

# print out with colors the things inside the app
print("The final appstate:")
cprint(vars(app))
