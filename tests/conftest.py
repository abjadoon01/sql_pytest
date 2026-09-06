import pytest
from order_app import OrderDatabase, OrderService, Product, ProductRegistry


@pytest.fixture
def database(tmp_path):
    db_path = tmp_path / "test_orders.db"
    db = OrderDatabase(db_path)
    db.create_tables()
    yield db


@pytest.fixture
def service_order(database):
    product = Product(
        name="Blender",
        price=120,
        stock=4
    )

    registry = ProductRegistry()
    registry.add_product(product)

    service = OrderService(registry, database)

    yield service, database, product