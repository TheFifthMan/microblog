from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {"username" : "John Wen"}
    posts = [
        {
            "author":{ "username" : "susan" },
            "body": "Hello World",
        },
        {
            "author":{ "username" : "jack" },
            "body": "Hello World jack",
        }
    ]
    return render_template('index.html',title="Home", user=user,posts=posts)