from models.Quiz import Quiz
from helpers.cprint import cprint

from helpers.fake import apiQuestions

myQuiz = Quiz()
myQuiz.addQuestion()

cprint(vars(myQuiz))
cprint(apiQuestions(1))
