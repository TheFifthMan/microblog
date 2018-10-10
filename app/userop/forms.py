from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,ValidationError,Length,EqualTo,Email
from .models import User

class EditProfileForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    #email = StringField('email',validators=[DataRequired(),Email()])
    about_me = TextAreaField('about me')
    submit = SubmitField('submit')

    def __init__(self,original_username,*args,**kw):
        super(EditProfileForm,self).__init__(*args,**kw)
        self.original_username = original_username


    def validate_username(self,username):
        if username != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('username exists')