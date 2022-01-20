import mongoengine

# mongodb://project:techmarket12@ds111063.mlab.com:11063/c4e20-project

host = "ds111063.mlab.com"
port = 11063
db_name = "c4e20-project"
user_name = "project"
password = "techmarket12"


def connect():
    mongoengine.connect(
        db_name, 
        host=host, 
        port=port, 
        username=user_name, 
        password=password
    )
def connect1():
    mongoengine.connect(
        db_name, 
        # alias='db1',
        # host='mongodb+srv://admin:admin@thanhcluster-soioj.mongodb.net/c4e20-project?retryWrites=true&w=majority',
        host='mongodb+srv://admin:admin@thanhcluster.soioj.mongodb.net/c4e20-project?retryWrites=true&w=majority',
        username='admin',
        password='admin'
    )
# def connect():
#     mongoengine.connect(
#         db_name, 
#         host='mongodb+srv://admin:admin@thanhcluster-soioj.mongodb.net/c4e20-project?retryWrites=true&w=majority',
#         username='admin',
#         password='admin'
#     )

from models.product import Product
from mongoengine.context_managers import switch_db

if __name__ == "__main__":
    connect()
    connect1()
    all_products = Product.objects()

    with switch_db(Product, 'db1') as Product:
        for i in range(len(all_products)):
            Product(**all_products[i].to_dict()).save()
            print("add product", i)

