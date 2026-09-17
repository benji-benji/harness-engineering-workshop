from shop.errors import AppError
from shop.repositories import orders as orders_repository
from shop.repositories.orders import Order, OrderLine

SHIPPING_PENCE = 399
FREE_SHIPPING_THRESHOLD_PENCE = 5000


def calculate_total(lines: list[OrderLine], discount_pence: int = 0) -> int:
    subtotal = 0
    for line in lines:
        subtotal = subtotal + line.quantity * line.unit_price_pence
    discounted = max(subtotal - discount_pence, 0)
    if discounted >= FREE_SHIPPING_THRESHOLD_PENCE:
        return discounted
    return discounted + SHIPPING_PENCE


def place_order(customer: str, lines: list[OrderLine], discount_pence: int = 0) -> Order:
    if not lines:
        raise AppError("An order needs at least one line")
    if any(line.quantity < 1 or line.unit_price_pence < 0 for line in lines):
        raise AppError("Quantities must be at least 1 and prices must not be negative")
    if discount_pence < 0:
        raise AppError("A discount must not be negative")
    order_id = orders_repository.create_order(customer, lines, discount_pence)
    return get_order(order_id)


def get_order(order_id: int) -> Order:
    order = orders_repository.get_order(order_id)
    if order is None:
        raise AppError(f"Order {order_id} not found", status_code=404)
    return order


def cancel_order(order_id: int) -> Order:
    order = get_order(order_id)
    if order.status == "cancelled":
        raise AppError(f"Order {order_id} is already cancelled", status_code=409)
    orders_repository.set_status(order_id, "cancelled")
    return get_order(order_id)
