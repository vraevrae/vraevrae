from flask import Flask, Blueprint, flash, redirect, render_template, request, session, url_for
from flask_session import Session

app = Flask(__name__)
quiz = Blueprint('quiz', __name__)


@quiz.route('/<page>')
def show(page):
    return page
