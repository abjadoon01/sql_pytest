import pytest
from order_app import Product


@pytest.fixture
def product():
    product = Product(name= 'Blender', price=299.99, stock=9)
    yield product


def test_reduce_stock(product):
    product.reduce_stock(3)
    assert product.stock == 6

@pytest.mark.parametrize(
    "quantity, expected",
    [
        (5, 4),
        (7, 2),
    ]
)
def test_reduce_stock_exact_amount(quantity, expected, product):
    product.reduce_stock(quantity)
    assert product.stock == expected

@pytest.mark.parametrize("quantity", [10, 0, -5])
def test_reduce_stock_errors(quantity, product):
    with pytest.raises(ValueError):    
        product.reduce_stock(quantity)


