from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Email
class LoginForm(FlaskForm):
	username=StringField('Username',validators=[Email('EMAIL TO DHANG SE LIKH')])
	password=PasswordField('Password',validators=[DataRequired()])
	remember_me = BooleanField('Remember me')
	submit= SubmitField('Log in')
