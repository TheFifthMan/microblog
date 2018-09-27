from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),index=True,unique=True)
    email = db.Column(db.String(128),index=True,unique=True)
    password_hash = db.Column(db.String(256))

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


    