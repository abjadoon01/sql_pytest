import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from order_app import (OrderDatabase, OrderRequest, OrderService, Product,
                       ProductRegistry)
from pydantic import ValidationError

logging.basicConfig(filename="app.log", level=logging.DEBUG, format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
load_dotenv()
db_name = os.getenv('DATABASE_NAME')


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents= True, exist_ok= True)
DB_PATH = DATA_DIR / db_name
database = OrderDatabase(DB_PATH)

data = {
    "customer_name": "Ali",
    "product_name": "Blender",
    "quantity": 2
}
data_1 = {
    "customer_name": "Ali",
    "product_name": "Blender",
    "quantity": 3
}
data_2 = {
    "customer_name": "Alice",
    "product_name": "Food Processor",
    "quantity": 2
}
try: 
    order = OrderRequest(**data)    
    order_1 = OrderRequest(**data_1) 
    order_2 = OrderRequest(**data_2) 

except ValidationError as e:
    print(str(e))

product1= Product(name= 'Blender', price= 89.99, stock= 4)
product2= Product(name= 'Food Processor', price= 129.99, stock= 2)
register_product = ProductRegistry()
register_product.add_product(product1)
register_product.add_product(product2)
database.create_tables()
service = OrderService(register_product, database)
print(service.process_order(order))
print(service.process_order(order_1))
print(service.process_order(order_2))
print(database.get_orders())
