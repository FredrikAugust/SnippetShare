"""Simple social networking _thing_ to show you code snippets"""

__author__ = 'Fredrik A. Madsen-Malmo'

import datetime

from peewee import *
from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash
from flask.ext.bcrypt import check_password_hash

DATABASE = SqliteDatabase('socialen.db')

class User(UserMixin, Model):
	email = CharField(unique=True)
	password = CharField(max_length=100)
	joined = DateTimeField(default=datetime.datetime.now)
	is_admin = BooleanField(defualt=false)

	class Meta:
		database = DATABASE
		order_by = ('-joined_at',)

	@classmethod
	def create_user(cls, email, password, admin=False):
		try:
			cls.create(
				email=email,
				password=generate_password_hash(password),
				is_admin=admin
			)
		except IntegrityError:
			raise ValueError("User already exists.")