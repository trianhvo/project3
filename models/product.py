from mongoengine import *
from models.helper import mongo_to_dict

class Product(Document):
    image = StringField()
    name = StringField()
    product_type = StringField()
    description = StringField()
    price = IntField()
    status = StringField()
    place = StringField()
    def to_dict(self):
        return mongo_to_dict(self)