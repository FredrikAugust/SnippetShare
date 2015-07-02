"""This is the main app, this is basically where shit goes wrong 
when trying to publish the app to heroku.
"""

__author__ = 'Fredrik A. Madsen-Malmo'

from flask import Flask
from flask import g
from flask.ext.login import LoginManager

import models

DEBUG = True
PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = ';abrov]pwdjoeiw9g-20[34I)(U)*(&T%*^&%^$aay38794809#$xertcfhgvjkhbLVKGHFHGB]]]}{><?'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	"""This is used by PeeWee to check if the user exists or not."""
	try:
		return models.User.get(models.User.id == user_id)
	except models.DoesNotExist:
		return None

@app.before_request
def before_request():
	"""Connect to db before each req"""
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	"""Close the db connection after each req"""
	g.db.close()

	return response

if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT, host=HOST)