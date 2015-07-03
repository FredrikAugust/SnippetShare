"""This is the python file ot hold all the code
regarding interaction with forms
"""

__author__ = 'Fredrik A. Madsen-Malmo'

from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError,	
								Email, Length, EqualTo)

from models import User
from languages import LANGUAGES

def email_exist(form, field):
	"""This is a custom validatior used above.
	It checks if the email already exists.
	"""
	if User.select().where(User.email == field.data).exists():
		raise ValidationError('That email is already taken.')

class RegisterForm(Form):
	"""Validation for the registration form.
	I decided not to use a username field as I feel it is 
	unnecessary
	"""
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

class LoginForm(Form):
	"""Validation for the registration form.
	I decided not to use a username field as I feel it is 
	unnecessary
	"""
	email = StringField(
		'email',
		validators=[
			DataRequired(),
			Email()
		]
	)
	password = PasswordField(
		'password',
		validators=[
			DataRequired()
		]
	)

class PostForm(Form):
	content = TextAreaField(
		'Share your snippet with the world',
		validators=[
			DataRequired()
		]
	)
	explanation = TextAreaField(
		'Care to explain?',
		validators=[
			DataRequired()
		]
	)
	language = SelectField(
		'Select syntax highlighting',
		choices=LANGUAGES
	)
