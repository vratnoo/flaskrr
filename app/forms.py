from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import ValidationError,DataRequired,Email,EqualTo
from app.models import User

class RegistrationForm(FlaskForm):
	username= StringField('usernmae',validators=[DataRequired()])
	email= StringField('email',validators=[Email()])
	password = PasswordField('password',validators=[DataRequired()])
	password2 = PasswordField('repeat_password',validators=[EqualTo('password')])
	submit = SubmitField('Submit')

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different USER  NAME')
	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email')



class LoginForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired()])
	password=PasswordField('Password',validators=[DataRequired()])
	remember_me = BooleanField('Remember me')
	submit= SubmitField('Log in')
