from flask_wtf import FlaskForm
from wtforms import SubmitField,TextAreaField
from wtforms.validators import DataRequired,ValidationError,Length,EqualTo,Email
from app.models import User,Post

class PostForm(FlaskForm):
    body = TextAreaField('Say Something.',validators=[DataRequired(),Length(1,140)])
    submit = SubmitField('Submit')
