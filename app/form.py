from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.validators import Length
import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = db.session.scalar(
            sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username')
        
    def validate_email(self, email):
        user = db.session.scalar(
            sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address')
        

class EditProfileForm(FlaskForm):
    """form for editing profile"""
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
            
    def validate_username(self, username):
        if self.original_username != username.data:
            user = db.session.scalar(
                sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username')

    
class EmptyForm(FlaskForm):
    """Form for the follow and unfollow button"""
    submit = SubmitField('Submit')
    
    
class PostForm(FlaskForm):
    """Form to create new posts"""
    post = TextAreaField('Say Sometting ', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
    

class ResetPasswordRequestForm(FlaskForm):
    """Form for reseting password when foirgotten"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
