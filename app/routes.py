from app import app,db
from flask import render_template,redirect,url_for,flash,request
from  .forms import LoginForm,RegisterForm,EditProfileForm
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.urls import url_parse
from .models import User,Post
from datetime import datetime 


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


@app.route('/logut')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login',methods=['GET',"POST"])
def login():
    if current_user.is_authenticated:
        flash("You have login")
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #flash("Login requested for user {}, remember me = {}".format(form.username.data,form.remember_me.data))
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user,remember=form.remember_me.data)
            flash('Login successful. Your username is {}'.format(user.username))
            return redirect(url_for('index'))

        flash('Invilida username or password.')
        # 本身就是一个网址
        next_page = request.args.get('next')
        if next_page is not None and url_parse(next_page).netloc != '':
            # 如果是外部连接，就自动跳转到首页
            next_page = url_for('index')
        
        return redirect(next_page)

    return render_template('login.html',title='login',form=form)


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('You have login')
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data,email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Conguration! You have the part of this site.')
        return redirect(url_for('login'))

    return render_template('register.html',title='register',form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {
            'author':user,
            'body':'Hello tester',
        },
          {
            'author':user,
            'body':'Hello tester2',
        },
    ]

    return render_template('user.html',user=user,posts=posts)

@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():

    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('You have changed your profile.')
        return redirect(url_for('user',username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    
    return render_template('edit_profile.html',title='edit profile',form=form)


    
