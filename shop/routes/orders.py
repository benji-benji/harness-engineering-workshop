from fastapi import APIRouter
from pydantic import BaseModel

from shop.services import orders as orders_service
from shop.services.orders import Order, OrderLine

router = APIRouter(prefix="/orders", tags=["orders"])


class LineIn(BaseModel):
    sku: str
    quantity: int
    unit_price_pence: int


class OrderIn(BaseModel):
    customer: str
    lines: list[LineIn]
    discount_pence: int = 0


class OrderOut(BaseModel):
    id: int
    customer: str
    status: str
    total_pence: int


def to_order_out(order: Order) -> OrderOut:
    return OrderOut(
        id=order.id,
        customer=order.customer,
        status=order.status,
        total_pence=orders_service.calculate_total(order.lines, order.discount_pence),
    )


@router.post("", status_code=201)
def create_order(body: OrderIn) -> OrderOut:
    lines = [OrderLine(**line.model_dump()) for line in body.lines]
    return to_order_out(orders_service.place_order(body.customer, lines, body.discount_pence))


@router.get("/{order_id}")
def read_order(order_id: int) -> OrderOut:
    return to_order_out(orders_service.get_order(order_id))


@router.post("/{order_id}/cancel")
def cancel_order(order_id: int) -> OrderOut:
    return to_order_out(orders_service.cancel_order(order_id))
