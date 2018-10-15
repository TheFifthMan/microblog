from app.userop import user_bp
from app import db
from flask import render_template,redirect,url_for,flash,request,current_app
from  .forms import EditProfileForm
from flask_login import login_required,current_user
from app.models import User
from datetime import datetime 


@user_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()

@user_bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1,type=int)
    posts = user.posts.paginate(page,current_app.config['PAGINATE_PER_PAGE'],False)
    prev_url = url_for('userop.user',username=username,page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('userop.user',username=username,page=posts.next_num) if posts.has_next else None

    return render_template('userop/user.html',title='user',user=user,prev_url=prev_url,next_url=next_url,posts=posts.items)

@user_bp.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('You have changed your profile.')
        return redirect(url_for('userop.user',username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    
    return render_template('userop/edit_profile.html',title='edit profile',form=form)


@user_bp.route('/follow/<username>')
@login_required
def follow(username):
    u = User.query.filter_by(username=username).first()
    if u == current_user:
        flash('You can\'t follow yourself.' )
        return redirect(url_for('userop.user',username=username))

    if u is None:
        flash('user dont exists. ')
        return redirect(url_for('main.index'))

    if current_user.is_following(u):
        flash("You are following")
        return redirect(url_for('main.index'))
        
    current_user.follow(u)
    db.session.commit()
    flash('You are followed this user')
    return redirect(url_for('userop.user',username=username))

@user_bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        flash('user dont exists')
        return redirect(url_for('main.index'))

    if current_user.is_following(u):
        current_user.unfollow(u)
        db.session.commit()
        flash('You have unfollowed this user')
        return redirect(url_for('userop.user',username=username))

    flash('You haven\'t followed this user' )
    return redirect(url_for('main.index'))

@user_bp.route('/user/<username>/<popup>')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return render_template()
    else:
        return redirect('main.index')