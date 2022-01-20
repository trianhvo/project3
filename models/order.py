from mongoengine import *
from models.user import User
from models.product import Product
from models.shipper import Shipper

class Order(Document):
    user_id = ListField(ReferenceField(User))
    product_id = ListField(ReferenceField(Product))
    shipper_id = ListField(ReferenceField(Shipper))
    address = StringField()
    request_time = DateTimeField()
    order_time = DateTimeField()
    order_fee = IntField()
    ship_fee = IntField()
    is_ordered = BooleanField()
    status = StringField()