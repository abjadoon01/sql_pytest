from order_app import OrderRequest


def test_order_process(service_order):
    service, db, product = service_order

    request = OrderRequest(
        customer_name="Ali",
        product_name="Blender",
        quantity=2
    )

    total = service.process_order(request)

    orders = db.get_orders()

    assert total == 240
    assert product.stock == 2
    assert len(orders) == 1

    order = orders[0]

    assert order["name"] == "Ali"
    assert order["product_name"] == "Blender"
    assert order["quantity"] == 2
    assert order["unit_price"] == 120
    assert order["total"] == 240