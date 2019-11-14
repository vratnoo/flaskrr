from app import db


class User(db.Model):
	"""docstring for User"""
	ids = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(128))
	password = db.Column(db.String(128))

	def __repr__(self):
		return '<User {}>'.format(self.username) 
