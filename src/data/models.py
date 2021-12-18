from peewee import Model, DateTimeField, ForeignKeyField, CharField, SqliteDatabase
import datetime

db = SqliteDatabase("../database.db")


class BaseTable(Model):
    class Meta:
        database = db


class User(BaseTable):
    username = CharField(null=False, default='anonymous', index=True)
    password = CharField(null=False, max_length=64)


class Timetable(BaseTable):
    student = ForeignKeyField(User, null=False)
    date = DateTimeField(null=False, default=datetime.datetime.today())


if __name__ == "__main__":
    pass