from app import db,login_manager,app
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt
from time import time 


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# 新建一个联合表
followers = db.Table('followers',
    db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))
)


class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),index=True,unique=True)
    email = db.Column(db.String(128),index=True,unique=True)
    about_me = db.Column(db.String(256))
    last_seen = db.Column(db.DateTime,default=datetime.now)
    password_hash = db.Column(db.String(256))
    followed = db.relationship('User',secondary=followers,
                primaryjoin=(followers.c.follower_id == id),
                secondaryjoin=(followers.c.followed_id == id),
                backref=db.backref('followers',lazy='dynamic'), #这里的backref是一个表
                lazy='dynamic')
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    def follow(self,user):
        return self.followed.append(user)
    
    def unfollow(self,user):
        return self.followed.remove(user)

    
    # 涉及两个用法
    # 1. join的用法
    # 2. union的用法

    def followed_posts(self):
        followed = Post.query.join(
            followers,(followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id = self.id)

        return followed.union(own).order_by(Post.timestamp.desc())


    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def avatars(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return  'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)

    
    def get_reset_password_token(self,expires_in=600):
        return jwt.encode({'reset_password':self.id,'exp':time() + expires_in},
            app.config['SECRET_KEY'],algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
        except:
            return 
        return User.query.get(id)


    def __repr__(self):
        return "<User : {}>".format(self.username)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.now) 
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Post : {} >".format(self.body)


    