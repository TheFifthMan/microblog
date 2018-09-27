from app import app
from flask import render_template,redirect,url_for,flash
from  .forms import LoginForm

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


@app.route('/login',methods=['GET',"POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for user {}, remember me = {}".format(form.username.data,form.remember_me.data))
        return redirect(url_for('index'))

    return render_template('login.html',title='login',form=form)