from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import ValidationError,DataRequired,Email,EqualTo,length
from app.models import User
from  flask_login import current_user
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

#for editing profile
class EditProfileForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	about_me = TextAreaField('About me', validators=[length(min=0,max=140)])
	submit = SubmitField('Submit')
	# overloaded constructor to solve duplicate username problem
	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username
	
	def validate_username(self,username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=username.data).first()
			if user is not None:
				raise ValidationError('Please use a different USER  NAME')
