import os

class Config(object):
	"""docstring for config"""
	SECRET_KEY=os.environ.get('SECRET_KEY') or "KRICODE"