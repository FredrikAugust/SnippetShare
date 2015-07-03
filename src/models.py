"""Simple social networking _thing_ to show you code snippets"""

__author__ = 'Fredrik A. Madsen-Malmo'

import datetime

from peewee import *
from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash

DATABASE = SqliteDatabase('socialen.db')

class User(UserMixin, Model):
	email = CharField(unique=True)
	password = CharField(max_length=100)
	joined_at = DateTimeField(default=datetime.datetime.now)
	is_admin = BooleanField(default=False)

	class Meta:
		database = DATABASE
		order_by = ('-joined_at',)

	def get_posts(self):
		return Post.select().where(Post.user == self)

	def get_stream(self):
		return Post.select().where(
			(Post.user == self)
		)

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

class Post(Model):
	timestamp = DateTimeField(default=datetime.datetime.now)
	user = ForeignKeyField(
		rel_model=User,
		related_name='posts'
	)
	content = TextField()

	class Meta:
		database = DATABASE
		order_by = ('-timestamp',)

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User], safe=True)
	DATABASE.close()
