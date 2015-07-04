"""Simple social networking _thing_ to show you code snippets"""

__author__ = 'Fredrik A. Madsen-Malmo'

import datetime

from peewee import *
from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash

DATABASE = SqliteDatabase('snippetshare.db')

class User(UserMixin, Model):
	username = CharField(unique=True)
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
			(Post.user << self.get_following()) |
			(Post.user == self)
		)

	def get_following(self):
		return (
			User.select().join(
				Relationship, on=Relationship.to_user
			).where(
				Relationship.from_user == self
			)
		)

	def get_followers(self):
		return (
			User.select().join(
				Relationship, on=Relationship.from_user
			).where(
				Relationship.to_user == self
			)
		)

	@classmethod
	def create_user(cls, username, password, admin=False):
		try:
			cls.create(
				username=username,
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
	language = TextField()
	display_language = TextField()

	class Meta:
		database = DATABASE
		order_by = ('-timestamp',)

class Relationship(Model):
	from_user = ForeignKeyField(
		User,
		related_name='relationships'
	)
	to_user = ForeignKeyField(
		User,
		related_name='related_to'
	)

	class Meta:
		database = DATABASE
		indexes = (
			(('from_user', 'to_user'), True),
		)

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Post, Relationship], safe=True)
	DATABASE.close()
