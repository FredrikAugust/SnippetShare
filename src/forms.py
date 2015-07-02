"""This is the python file ot hold all the code
regarding interaction with forms
"""

__author__ = 'Fredrik A. Madsen-Malmo'

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError,	
								Email, Length, EqualTo)

from models import User

class RegisterForm(Form):
	email = StringField(
		'email',
		validators=[
			DataRequired(),
			Email(),
			email_exist  # Custom validator
		]
	)
	password = PasswordField(
		'password',
		validators=[
			DataRequired(),
			Length(min=4),
			EqualTo('password2', message='Passwords must match.')
		]
	)
	password2 = PasswordField(
		'retype password',
		validators=[
			DataRequired()
		]
	)


def email_exist(form, field):
	"""This is a custom validatior used above.
	It checks if the email already exists.
	"""
	if User.select().where(User.email == field.data).exists():
		raise ValidationError('That email is already taken.')