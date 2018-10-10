from app.main import main_bp
from app import db
from flask import render_template,redirect,url_for,flash,request
from  .forms import PostForm
from flask_login import login_required,current_user
from werkzeug.urls import url_parse
from .models import User,Post


@main_bp.route('/',methods=['GET','POST'])
@main_bp.route('/index',methods=['GET','POST'])
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

    return render_template('main/index.html',title="Home",form=form,next_url=next_url,prev_url=prev_url,posts=posts.items)

@main_bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,app.config['PAGINATE_PER_PAGE'],False)
    prev_url = url_for('explore',page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('explore',page=posts.next_num) if posts.has_next else None
    return render_template('main/index.html',title="explore",next_url=next_url,prev_url=prev_url,posts=posts.items)
