from app.schemas.order import OrderIn

def test_order_schema():
    o = OrderIn(buyer_id="b", product_id="p", amount=10.5)
    assert o.amount == 10.5
