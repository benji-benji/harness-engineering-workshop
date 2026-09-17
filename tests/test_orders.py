import pytest
from fastapi.testclient import TestClient

from shop.app import app
from shop.errors import AppError
from shop.repositories.orders import OrderLine
from shop.services import orders as orders_service

client = TestClient(app)


def test_total_sums_every_line_and_adds_shipping() -> None:
    lines = [OrderLine("mug", 2, 750), OrderLine("pen", 3, 120)]
    assert orders_service.calculate_total(lines) == 1500 + 360 + 399


def test_total_has_free_shipping_at_the_threshold() -> None:
    lines = [OrderLine("lamp", 1, 3000), OrderLine("desk tidy", 2, 1000)]
    assert orders_service.calculate_total(lines) == 5000


def test_total_applies_the_discount_before_shipping() -> None:
    lines = [OrderLine("lamp", 2, 3000)]
    assert orders_service.calculate_total(lines, discount_pence=2000) == 4000 + 399


def test_discount_cannot_make_the_total_negative() -> None:
    assert orders_service.calculate_total([OrderLine("pen", 1, 120)], discount_pence=500) == 399


def test_placing_an_order_without_lines_is_an_error() -> None:
    with pytest.raises(AppError):
        orders_service.place_order("ada", [])


def test_create_and_read_an_order_over_http() -> None:
    created = client.post(
        "/orders",
        json={"customer": "ada", "lines": [{"sku": "mug", "quantity": 2, "unit_price_pence": 750}]},
    )
    assert created.status_code == 201
    assert created.json()["total_pence"] == 1899
    fetched = client.get(f"/orders/{created.json()['id']}")
    assert fetched.json() == created.json()


def test_unknown_order_is_a_404() -> None:
    response = client.get("/orders/999")
    assert response.status_code == 404
    assert response.json() == {"error": "Order 999 not found"}


def test_cancelling_twice_is_a_conflict() -> None:
    order = orders_service.place_order("ada", [OrderLine("mug", 1, 750)])
    assert orders_service.cancel_order(order.id).status == "cancelled"
    assert client.post(f"/orders/{order.id}/cancel").status_code == 409
