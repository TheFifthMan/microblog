from app.auth import auth_bp
from app import db
from flask import render_template,redirect,url_for,flash,request
from  .forms import LoginForm,RegisterForm,ReuqestRestPasswdForm,ResetPasswordForm
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.urls import url_parse
from app.models import User,Post
from datetime import datetime 
from app.email import send_reset_password_email


@auth_bp.route('/logut')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/login',methods=['GET',"POST"])
def login():
    if current_user.is_authenticated:
        flash("You have login")
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        #flash("Login requested for user {}, remember me = {}".format(form.username.data,form.remember_me.data))
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user,remember=form.remember_me.data)
            flash('Login successful. Your username is {}'.format(user.username))
            return redirect(url_for('main.index'))

        flash('Invilida username or password.')
        # 本身就是一个网址
        next_page = request.args.get('next')
        if next_page is not None and url_parse(next_page).netloc != '':
            # 如果是外部连接，就自动跳转到首页
            next_page = url_for('main.index')
        
        return redirect(next_page)

    return render_template('auth/login.html',title='login',form=form)


@auth_bp.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('You have login')
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data,email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Conguration! You have the part of this site.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',title='register',form=form)


@auth_bp.route('/request-reset-passwd',methods=["GET","POST"])
def request_reset_passwd():
    if current_user.is_authenticated:
        flash('You have login')
        return redirect(url_for('main.index'))
    form = ReuqestRestPasswdForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('send email successful')
            send_reset_password_email(user)
        else:
            flash('check your email')
            return redirect(url_for('auth.request_reset_passwd'))
    
    return render_template('auth/request_reset_passwd.html',title='request reset password',form=form)

@auth_bp.route('/reset-passwd/<token>',methods=["GET","POST"])
def reset_passwd(token):
    user = User.verify_reset_password_token(token)
    if user is None:
        flash('The token is error or expire')
        return redirect(url_for('main.index'))
    
    if current_user.is_authenticated:
        flash('You have login. ')
        return redirect(url_for('main.index'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('You have change your password. Please Login')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',title='reset password',form=form)