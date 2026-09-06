import pytest
from order_app import OrderDatabase


@pytest.fixture
def database(tmp_path):
    db_path = tmp_path / "test_orders.db"
    db = OrderDatabase(db_path)
    db.create_tables()
    yield db

def test_duplicate_customer(database):
    customer_id_1 = database.save_customer('Ali')
    customer_id_2 = database.save_customer('Ali')
    assert isinstance(customer_id_1, int)
    assert customer_id_1 == customer_id_2

def test_insert_customer(database):
    customerid = database.save_customer('Ali')
    database.save_order(customerid, product_name= 'Blender', quantity= 2 , unit_price= 120 , total= 240)  
    orders = database.get_orders()
    assert len(orders) == 1
    order = orders[0]
    assert order["name"] == "Ali"
    assert order["product_name"] == "Blender"
    assert order["quantity"] == 2
    assert order["unit_price"] == 120
    assert order["total"] == 240


