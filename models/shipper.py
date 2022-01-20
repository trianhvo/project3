from mongoengine import *

class Shipper(Document):
    fullname = StringField()
    phone = StringField()
    email = EmailField()
    id_person = IntField()
    birthday = DateTimeField()
    balance = IntField()
    username = StringField()
    password = StringField()