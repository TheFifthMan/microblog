# from flask_wtf import FlaskForm
# from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
# from wtforms.validators import DataRequired,ValidationError,Length,EqualTo,Email
# from .models import User,Post

# class PostForm(FlaskForm):
#     body = TextAreaField('Say Something.',validators=[DataRequired(),Length(1,140)])
#     submit = SubmitField('Submit')

# class ReuqestRestPasswdForm(FlaskForm):
#     email = StringField('Your email is: ',validators=[DataRequired()])
#     submit = SubmitField('submit')

# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('New Password: ',validators=[DataRequired(),Length(8,20)])
#     password2 = PasswordField("Enter Password Again: ",validators=[DataRequired(),Length(8,20),EqualTo('password')])
#     submit = SubmitField('submit')

# class LoginForm(FlaskForm):
#     username = StringField('username',validators=[DataRequired()],render_kw={
#         "type":"text",
#         "class":"form-control",
#         "placeholder":"Username",
#         "aria-describedby":"basic-addon1",
#     })
#     password = PasswordField('password',validators=[DataRequired()])
#     remember_me = BooleanField('remember me')
#     submit = SubmitField('submit')


# class RegisterForm(FlaskForm):
#     username = StringField('username',validators=[ DataRequired() ])
#     password = PasswordField('password',validators=[DataRequired(),Length(8,20)])
#     password2 = PasswordField('password2',validators=[DataRequired(),EqualTo("password")])
#     email = StringField('email',validators=[DataRequired(),Email()])
#     submit = SubmitField('submit')

#     def validate_username(self,username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('user exists.')


#     def validate_email(self,email):
#         email = User.query.filter_by(email=email.data).first()
#         if email:
#             raise ValidationError('email exists')

# class EditProfileForm(FlaskForm):
#     username = StringField('username',validators=[DataRequired()])
#     #email = StringField('email',validators=[DataRequired(),Email()])
#     about_me = TextAreaField('about me')
#     submit = SubmitField('submit')

#     def __init__(self,original_username,*args,**kw):
#         super(EditProfileForm,self).__init__(*args,**kw)
#         self.original_username = original_username


#     def validate_username(self,username):
#         if username != self.original_username:
#             user = User.query.filter_by(username=username.data).first()
#             if user:
#                 raise ValidationError('username exists')