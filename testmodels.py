from models.Quiz import Quiz
from helpers.cprint import cprint

from helpers.fake import apiQuestion

myQuiz = Quiz()
myQuiz.addQuestion(**apiQuestion())
myQuiz.addQuestion(**apiQuestion())
myQuiz.addQuestion(**apiQuestion())
myQuiz.addQuestion(**apiQuestion())
myQuiz.addQuestion(**apiQuestion())

cprint(vars(myQuiz))
