from datetime import date, datetime
from peewee import *
from .database import database_connection as database
import hashlib

class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username

    class Meta:
        database = database
        table_name = 'users'


    # Hashing the new user password
    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()

        h.update(password.encode('utf-8'))
        return h.hexdigest()


class Movie(Model):
    title = CharField(max_length=100)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

    class Meta:
        database = database
        table_name = 'movies'

class UserReview(Model):
    user = ForeignKeyField(User, backref='reviews')
    movies = ForeignKeyField(Movie, backref='reviews')
    review = TextField()
    score = IntegerField()
    created_at = DateField(default=datetime.now)

    def __str__(self):
        return f'{self.user.username} - {self.movies.title}'

    class Meta:
        database = database
        table_name = 'user_reviews'