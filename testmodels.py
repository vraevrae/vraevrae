from models.App import App
from helpers.cprint import cprint

app = App()
app.newQuiz()

cprint(vars(app))
