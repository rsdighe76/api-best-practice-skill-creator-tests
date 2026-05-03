# ACME Orders API — Common Workflows

Read this file when: you need to chain multiple API calls together — onboarding a customer, placing an order, managing lifecycle, or recovering from failures.

---

## 1. Create a Customer Without Duplicates

**When to use:** Any time you can't guarantee the create hasn't already run (network timeout, process restart, retry).

POST /customers is **not idempotent** — a naive retry creates a duplicate.

1. `GET /customers?email=<email>&limit=1` — check whether the customer exists
   - `data` non-empty → extract `id`, skip to step 3
   - `data` empty → proceed to step 2
2. `POST /customers` — extract `id` from the 201 response
3. Use the returned `id` for subsequent calls

**Recovery:** If step 2 fails mid-flight, re-run step 1 before retrying.

```python
def get_or_create_customer(name, email):
    resp = GET("/customers", params={"email": email, "limit": 1})
    if resp["data"]:
        return resp["data"][0]["id"]
    return POST("/customers", json={"name": name, "email": email})["id"]
```

---

## 2. Full Checkout — Onboard Customer and Place First Order

**When to use:** End-to-end first purchase by a new customer.

1. `GET /customers?email=<email>&limit=1` — check if customer exists (see Workflow 1)
2. `POST /customers` if not found — extract `customer_id`
3. Generate and **persist** an `Idempotency-Key` **before** calling the API
4. `POST /orders` with `customer_id`, `items[]`, and `Idempotency-Key`

**Recovery:** If step 4 fails, reuse the same key — server returns cached result if order was already created.

---

## 3. Paginate Through All Orders for a Customer

**When to use:** Fetching complete order history, reports, or checking for open orders before deletion.

```python
def get_all_orders(customer_id, status=None):
    cursor, results = None, []
    while True:
        params = {"customer_id": customer_id, "limit": 100}
        if cursor:
            params["cursor"] = cursor
        if status:
            params["status"] = status
        resp = GET("/orders", params=params)
        results.extend(resp["data"])
        cursor = resp.get("next_cursor")
        if not cursor:
            break
    return results
```

Always use `limit=100` — the default of 20 means 5× more requests for a customer with 100 orders.

---

## 4. Advance an Order Through Its Lifecycle

**When to use:** Moving an order from `created` → `paid` → `fulfilled` as events arrive.

| From | To | When |
|------|----|------|
| `created` | `paid` | Payment confirmed |
| `paid` | `fulfilled` | Order shipped |
| `created` or `paid` | `cancelled` | Order cancelled |

1. `GET /orders/{order_id}` — confirm current status; if already at target, treat as success
2. Generate and persist an `Idempotency-Key`
3. `PATCH /orders/{order_id}` with `{"status": "<next>"}` and key

**Constraint:** Cannot skip states — `created → fulfilled` is rejected. Go through `paid` first.

**Recovery:** Reuse the same key on retry — server returns cached result if transition already happened.

---

## 5. Delete a Customer Safely

**When to use:** Removing a customer. DELETE /customers is **permanent and irreversible**.

The API returns 409 if the customer has active orders — cancel them first.

1. `get_all_orders(customer_id, status="created")` — paginate fully
2. `DELETE /orders/{order_id}` for each → expect 204
3. Repeat for `status="paid"`
4. `DELETE /customers/{customer_id}` → expect 204

**Recovery:** 409 on step 4 means an order is still active. Re-run steps 1–3, then retry.

---

## 6. Recover a Failed Write

**When to use:** POST or PATCH returned a network error or 5xx and you don't know if it succeeded.

**Endpoints with idempotency** (POST /orders, PATCH /customers, PATCH /orders):
- Reuse the exact same `Idempotency-Key` and retry — server returns cached result

**POST /customers (no idempotency):**
1. `GET /customers?email=<email>` — check if it was created
2. Found → use existing `id`, do not retry POST
3. Not found → retry POST

**Critical:** Persist the key **before** the API call, not after.
