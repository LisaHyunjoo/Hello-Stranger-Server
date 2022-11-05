from peewee import *
import datetime

DATABASE = SqliteDatabase('dogs.sqlite')

class Post(Model):
    title = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Post], safe=True)
    print('created tables')
    DATABASE.close()
