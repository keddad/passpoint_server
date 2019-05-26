from peewee import *
import datetime

db = PostgresqlDatabase(
    'postgred_db',
    user='gaybar',
    password='IM A 1EE7 HAckER',
    host=' 5.8.180.39'
)  # Should be used normally. but we shouldn't use it for testing

db = SqliteDatabase('test.db')  # Model for local testing


class SignedDocument(Model):
    """
    Model used to save signed notes
    DeviceId - MD5 of Tablet's WiFi MAC
    Signature = MD5 of original File. Definately not the best solution. TODO
    """

    DeviceId = CharField()
    Place = CharField()

    FirstName = CharField()
    MiddleName = CharField()
    LastName = CharField()

    Signature = CharField()

    SignedDate = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db
