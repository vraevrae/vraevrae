from flask import Flask, Blueprint, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)
api = Blueprint('api', __name__)


@api.route('/<page>')
def show(page):
    return page
