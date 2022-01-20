from mongoengine import *

class User(Document):
    fullname = StringField()
    phone = StringField()
    email = EmailField()
    address = StringField()
    balance = IntField()
    username = StringField()
    password = StringField()