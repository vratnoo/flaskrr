import os
basdir= os.path.abspath(os.path.dirname(__file__))
class Config(object):
	"""docstring for config"""
	SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
	SECRET_KEY=os.environ.get('SECRET_KEY') or "KRICODE"