# Task 001. Order summary

Customer support want to see how an order's total was reached without doing the sum themselves.

Add `GET /orders/{order_id}/summary`. It returns JSON with these fields.

| Field | Meaning |
|---|---|
| `id` | The order's id |
| `status` | The order's status |
| `item_count` | The number of items, which is the sum of the quantities and not the number of lines |
| `subtotal_pence` | The sum of quantity times unit price over every line |
| `discount_pence` | The discount that was applied, which is never more than the subtotal |
| `shipping_pence` | The shipping charged, using the same rule as `calculate_total` |
| `total_pence` | What the customer pays |

## Requirements

1. The sums live in a new function, `summarise_order`, in `shop/services/orders.py`. The route only calls it and shapes the response.
2. `total_pence` equals what `calculate_total` returns for the same order. Do not write the shipping rule out a second time.
3. An unknown order id returns the same 404 as `GET /orders/{order_id}`.
4. Each field has a test. Include an order with a discount larger than its subtotal, and an order at the free shipping threshold.

## Notes

Support mostly look up orders that went wrong. A cancelled order is not charged, so its summary shows `shipping_pence` and `total_pence` as 0, and the other fields as they were. This is the one case where `total_pence` differs from `calculate_total`.

Do not change the response of any existing endpoint.
