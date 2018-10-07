from app import app,db
from flask import render_template,redirect,url_for,flash,request
from  .forms import LoginForm,RegisterForm,EditProfileForm,PostForm,ReuqestRestPasswdForm,ResetPasswordForm
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.urls import url_parse
from .models import User,Post
from datetime import datetime 
from app.email import send_reset_password_email


@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
@login_required
def index():
    page = request.args.get('page',1,type=int)
    posts = current_user.followed_posts().paginate(page,app.config['PAGINATE_PER_PAGE'],False)
    next_url = url_for('index',page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index',page=posts.prev_num) if posts.has_prev else None
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("publish successful.")
        return redirect(url_for('index'))

    return render_template('index.html',title="Home",form=form,next_url=next_url,prev_url=prev_url,posts=posts.items)

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,app.config['PAGINATE_PER_PAGE'],False)
    prev_url = url_for('explore',page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('explore',page=posts.next_num) if posts.has_next else None
    return render_template('index.html',title="expore",next_url=next_url,prev_url=prev_url,posts=posts.items)

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
    page = request.args.get('page',1,type=int)
    posts = user.posts.paginate(page,app.config['PAGINATE_PER_PAGE'],False)
    prev_url = url_for('user',username=username,page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('user',username=username,page=posts.next_num) if posts.has_next else None

    return render_template('user.html',user=user,prev_url=prev_url,next_url=next_url,posts=posts.items)

@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
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

# 容易造成CSRF攻击，或者蠕虫攻击

@app.route('/follow/<username>')
@login_required
def follow(username):
    u = User.query.filter_by(username=username).first()
    if u == current_user:
        flash('You can\'t follow yourself.' )
        return redirect(url_for('user',username=username))

    if u is None:
        flash('user dont exists. ')
        return redirect(url_for('index'))

    if current_user.is_following(u):
        flash("You are following")
        return redirect(url_for('index'))
        
    current_user.follow(u)
    db.session.commit()
    flash('You are followed this user')
    return redirect(url_for('user',username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        flash('user dont exists')
        return redirect(url_for('index'))

    if current_user.is_following(u):
        current_user.unfollow(u)
        db.session.commit()
        flash('You have unfollowed this user')
        return redirect(url_for('user',username=username))

    flash('You haven\'t followed this user' )
    return redirect(url_for('index'))

@app.route('/request-reset-passwd',methods=["GET","POST"])
def request_reset_passwd():
    if current_user.is_authenticated:
        flash('You have login')
        return redirect(url_for('index'))
    form = ReuqestRestPasswdForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('send email successful')
            send_reset_password_email(user)
        else:
            flash('check your email')
            return redirect(url_for('request_reset_passwd'))
    
    return render_template('request_reset_passwd.html',title='request reset password',form=form)

@app.route('/reset-passwd/<token>',methods=["GET","POST"])
def reset_passwd(token):
    user = User.verify_reset_password_token(token)
    if user is None:
        flash('The token is error or expire')
        return redirect(url_for('index'))
    
    if current_user.is_authenticated:
        flash('You have login. ')
        return redirect(url_for('index'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('You have change your password. Please Login')
        return redirect(url_for('login'))
    return render_template('reset_password.html',title='reset password',form=form)