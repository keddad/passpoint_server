from peewee import *
import datetime

db = PostgresqlDatabase(
    'postgres_db',
    user='gaybar',
    password='IM A 1EE7 HAckER',
    host=' 5.8.180.39'
)  # Should be used normally. but we shouldn't use it for testing

db = SqliteDatabase('test.db')  # Model for local testing


class SignedDocument(Model):
    """
    Model used to save signed notes
    DeviceId - MD5 of Tablet's WiFi MAC (Or Not, Complicated)
    Signature = Path to original file in signatures/
    """

    DeviceId = CharField()
    Place = CharField()

    FirstName = CharField()
    MiddleName = CharField(default="-")
    LastName = CharField()

    Signature = CharField()

    SignedDate = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db

