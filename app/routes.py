from app import app
from flask import render_template,flash,redirect, url_for
from app.forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
	other = [{'author':'vikramratnoo',
			 'book':'Homospaians'},
			 {'author':'chetanbhagat',
			 'book':'3 idiots'}]
	return render_template('index.html',title='what just the times',other=other)
@app.route('/login',methods=['GET','POST'])	
def login():
	form = LoginForm()
	if(form.validate_on_submit()):
		flash('LOGIN REQUESSTED FOR USER {}'.format(form.username.data))
		return redirect(url_for('index'))
	return render_template('login.html',title="Login",form=form)
