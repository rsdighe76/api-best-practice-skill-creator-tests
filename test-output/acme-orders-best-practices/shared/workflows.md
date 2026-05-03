# ACME Orders API — Common Workflows

---

## 1. Create a Customer Without Duplicates

**When to use:** Onboarding a new customer, or any time you can't guarantee the create request hasn't already been sent (e.g. after a network timeout).

POST /customers is **not idempotent** — a naive retry creates a duplicate. Always check first.

1. `GET /customers?email=<email>` — check whether the customer already exists
   - If `data` array is non-empty → customer exists, extract `id` and skip to step 3
   - If `data` is empty → proceed to step 2
2. `POST /customers` with `name` and `email`
   - Extract `id` from the `201` response
3. Use the returned `id` for subsequent order creation

**Recovery:** If step 2 fails mid-flight (network error, timeout), re-run step 1 before retrying. The customer may have been created even if you didn't receive the response.

```python
def get_or_create_customer(name: str, email: str) -> str:
    # Step 1: check first
    resp = GET("/customers", params={"email": email, "limit": 1})
    if resp["data"]:
        return resp["data"][0]["id"]

    # Step 2: create
    resp = POST("/customers", json={"name": name, "email": email})
    return resp["id"]
```

---

## 2. Place a First Order (Full Checkout Flow)

**When to use:** End-to-end checkout — new customer placing their first order.

1. `GET /customers?email=<email>` — check if customer exists (see Workflow 1)
2. `POST /customers` if not found — extract `customer_id`
3. Generate and store an `Idempotency-Key` for the order before calling the API
4. `POST /orders` with `customer_id`, `items[]`, and `Idempotency-Key`
   - Extract `order_id` and `status` (`created`) from the `201` response
5. `GET /orders/{order_id}` — confirm order is in `created` state before proceeding to payment

**Data flow:** `customer_id` from step 2 → `POST /orders` body in step 4.

**Recovery:** If step 4 fails, reuse the same `Idempotency-Key` on retry — the server returns the cached result if the order was already created.

---

## 3. Paginate Through All Orders for a Customer

**When to use:** Fetching a complete order history; generating reports; checking for open orders before deletion.

```python
def get_all_orders(customer_id: str, status: str = None) -> list:
    cursor = None
    all_orders = []

    while True:
        params = {"customer_id": customer_id, "limit": 100}
        if cursor:
            params["cursor"] = cursor
        if status:
            params["status"] = status

        resp = GET("/orders", params=params)
        all_orders.extend(resp["data"])

        cursor = resp.get("next_cursor")
        if not cursor:
            break

    return all_orders
```

**Note:** Always use `limit=100` (the max) — the default of 20 means 5× more API calls for a customer with 100 orders.

---

## 4. Advance an Order Through Its Lifecycle

**When to use:** Moving an order from `created` → `paid` → `fulfilled` as payment and fulfilment events arrive.

Valid transitions:
| From | To | When |
|------|----|------|
| `created` | `paid` | Payment confirmed |
| `paid` | `fulfilled` | Order shipped/delivered |
| `created` or `paid` | `cancelled` | Customer or support cancels |

Steps:
1. `GET /orders/{order_id}` — confirm current `status` before transitioning
   - If already at target status → idempotent no-op, proceed
   - If in an incompatible state → do not proceed (e.g. can't mark `fulfilled` from `created`)
2. Generate an `Idempotency-Key` for this transition
3. `PATCH /orders/{order_id}` with `{"status": "<next_status>"}` and `Idempotency-Key`
   - Confirm the returned `status` matches the intended target

**Server constraint:** You cannot skip states — `created → fulfilled` in one step is not allowed; you must go through `paid` first.

**Recovery:** If the PATCH returns a network error or 5xx, reuse the same `Idempotency-Key` on retry. If it returns 409, a different payload was sent with that key — generate a new key and retry.

---

## 5. Delete a Customer Safely

**When to use:** Removing a customer record. This is **permanent and irreversible** — the customer and their data cannot be recovered.

You must cancel open orders before the customer can be deleted. The API will return `409` if the customer has active orders.

1. `GET /orders?customer_id=<id>&status=created` — fetch all open orders, paginate fully (see Workflow 3)
2. For each open order: `DELETE /orders/{order_id}` — cancel it
   - Expect `204 No Content`; handle `409` (already in a non-cancellable state)
3. `GET /orders?customer_id=<id>&status=paid` — repeat for paid orders if applicable
4. Cancel any paid orders (or confirm they are `fulfilled`/`cancelled` already)
5. `DELETE /customers/{customer_id}` — permanent deletion
   - Expect `204 No Content`

**Warning:** Step 5 is irreversible. Double-check the `customer_id` before calling.

**Recovery:** If step 5 returns `409`, at least one order is still in a non-cancelled state. Re-run steps 1–4 to find and cancel it, then retry step 5.

```python
def delete_customer_safely(customer_id: str) -> None:
    # Cancel all open orders first
    for status in ("created", "paid"):
        orders = get_all_orders(customer_id, status=status)
        for order in orders:
            resp = DELETE(f"/orders/{order['id']}")
            assert resp.status_code == 204, f"Failed to cancel order {order['id']}"

    # Now safe to delete
    resp = DELETE(f"/customers/{customer_id}")
    assert resp.status_code == 204
```

---

## 6. Recover a Failed Write

**When to use:** A POST or PATCH returned a network error, timeout, or 5xx, and you don't know if the server processed it.

**For endpoints that support `Idempotency-Key`** (POST /orders, PATCH /customers, PATCH /orders):
1. Reuse the exact same `Idempotency-Key` you sent originally
2. Retry the exact same request body
3. The server returns the cached result — no duplicate is created

**For POST /customers (no idempotency support):**
1. `GET /customers?email=<email>` — check if the customer was created
2. If found → use the existing `id`, do not retry the POST
3. If not found → retry the POST (the original request did not go through)

**Key rule:** Always store the `Idempotency-Key` **before** making the API call, not after. If you generate the key and then the process crashes, you need the key to safely retry.

```python
# Store key BEFORE the call
idempotency_key = str(uuid.uuid4())
db.save_pending_order(order_data, idempotency_key)  # persist first

# Then call the API
resp = POST("/orders", json=order_data,
            headers={"Idempotency-Key": idempotency_key})
```
