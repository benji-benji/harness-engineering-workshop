from dataclasses import dataclass

from shop.db import connect


@dataclass(frozen=True)
class OrderLine:
    sku: str
    quantity: int
    unit_price_pence: int


@dataclass(frozen=True)
class Order:
    id: int
    customer: str
    status: str
    discount_pence: int
    lines: list[OrderLine]


def create_order(customer: str, lines: list[OrderLine], discount_pence: int = 0) -> int:
    with connect() as connection:
        cursor = connection.execute(
            "INSERT INTO orders (customer, discount_pence) VALUES (?, ?)",
            (customer, discount_pence),
        )
        order_id = cursor.lastrowid
        assert order_id is not None
        connection.executemany(
            "INSERT INTO order_lines (order_id, sku, quantity, unit_price_pence)"
            " VALUES (?, ?, ?, ?)",
            [(order_id, line.sku, line.quantity, line.unit_price_pence) for line in lines],
        )
    return order_id


def get_order(order_id: int) -> Order | None:
    with connect() as connection:
        row = connection.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if row is None:
            return None
        line_rows = connection.execute(
            "SELECT sku, quantity, unit_price_pence FROM order_lines"
            " WHERE order_id = ? ORDER BY id",
            (order_id,),
        ).fetchall()
    return Order(
        id=row["id"],
        customer=row["customer"],
        status=row["status"],
        discount_pence=row["discount_pence"],
        lines=[OrderLine(**dict(line_row)) for line_row in line_rows],
    )


def set_status(order_id: int, status: str) -> None:
    with connect() as connection:
        connection.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
