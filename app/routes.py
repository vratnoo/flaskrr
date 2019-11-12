from app import app
from flask import render_template
@app.route('/')
def hello():
	return render_template('index.html',taa='what just the times')
@app.route('/<kri>')	
def hello2(kri):
	return "HELLO,WORLD"+kri
