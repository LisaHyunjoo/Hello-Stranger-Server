from peewee import *
import datetime
import os
from flask_login import UserMixin
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('posts.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique = True)
    password = CharField()

    class Meta:
        database = DATABASE


class Post(Model):
    user = ForeignKeyField(User, backref='posts')
    title = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class Comment(Model):
    user = ForeignKeyField(User, backref='comments' )
    post = ForeignKeyField(Post, backref='comments')
    content = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Comment, Post], safe=True)
    print('created tables')
    DATABASE.close()
