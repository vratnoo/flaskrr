from app import app
from flask import render_template
@app.route('/')
def hello():
	other = [{'author':'vikramratnoo',
			 'book':'Homospaians'},
			 {'author':'chetanbhagat',
			 'book':'3 idiots'}]
	return render_template('index.html',taa='what just the times',other=other)
@app.route('/<kri>')	
def hello2(kri):
	return "HELLO,WORLD"+kri
