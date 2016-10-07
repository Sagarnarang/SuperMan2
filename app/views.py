from app import app
from emai import main1
from flask import request

import nltk
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/fetchEmail')
def d():
    return str(main1())


@app.route("/signup")
def hello():
    return '<form action="/login" method="POST"><input name="username"><br><input name="password"><input type="submit" value="Echo"></form>'


@app.route("/login",methods=['POST'])
def echo():
    return "You said: " + request.form['username']+request.form['password']
