# ACME Orders API — Common Workflows

## 1. Create Customer Without Duplicates

**When to use:** Onboarding a new customer, or when you can't guarantee the create hasn't already been called (e.g. retrying after a network failure).

1. `GET /customers?email=<email>&limit=1` — check if the customer already exists by email
   - If `data` array is non-empty → use the existing `id`, skip to step 3
   - If empty → proceed to step 2
2. `POST /customers` with `name` and `email` (plus `company_name` / `vat_number` if required for your segment — see `endpoints/POST-v1-customers.md`)
   - Extract `id` from the response
3. Continue with the returned customer `id`

**Recovery:** `POST /customers` does not support idempotency keys. If step 2 fails mid-flight, always re-run step 1 before retrying — the customer may have been created.

---

## 2. Paginate Through All Customers or Orders

**When to use:** Any time you need the full list, not just the first page.

```python
cursor = None
results = []
while True:
    params = {"limit": 100}
    if cursor:
        params["cursor"] = cursor
    response = GET("/customers", params=params)  # or /orders
    results.extend(response["data"])
    cursor = response.get("next_cursor")
    if not cursor:
        break
```

Always use `limit=100` to minimise round trips. The default is 20, which means 5× more requests for large datasets.

---

## 3. Advance Order Through Lifecycle

**When to use:** Moving an order from `created` → `paid` → `fulfilled`, or cancelling it at any cancellable stage.

Valid transitions:
- `created` → `paid`: payment received
- `created` → `cancelled`: cancel before payment
- `paid` → `fulfilled`: order shipped or delivered
- `paid` → `cancelled`: cancel after payment (triggers refund)
- `fulfilled` → (terminal — no further transitions)
- `cancelled` → (terminal — no further transitions)

Steps:
1. `GET /orders/{order_id}` — confirm current `status` before transitioning
2. Generate and store a new `Idempotency-Key` (UUID v4) for this specific transition
3. `PATCH /orders/{order_id}` with `{"status": "<next_status>"}` and the stored key
   - Confirm the returned `status` matches what you sent

**Constraint:** Attempting an invalid transition (e.g. `fulfilled` → `paid`) returns 409. Always confirm current state in step 1 before transitioning.

**Recovery:** If the PATCH fails with a network error or 5xx, reuse the same `Idempotency-Key` to retry — the server returns the cached result if the transition already happened.

---

## 4. Delete Customer Safely

**When to use:** Permanently removing a customer record.

1. `GET /orders?customer_id=<id>&status=created&limit=1` — check for unpaid open orders
2. `GET /orders?customer_id=<id>&status=paid&limit=1` — check for paid but unfulfilled orders
3. For each open order found: `DELETE /orders/{order_id}` to cancel it (see workflow 5)
4. `DELETE /customers/{customer_id}` — permanent deletion, no undo

**Warning:** `DELETE /customers/{customer_id}` is irreversible. The customer record is permanently removed. If the customer has orders in `created` or `paid` status, the API returns 409.

---

## 5. Cancel an Order

**When to use:** Cancelling an order that is in `created` or `paid` status.

1. `GET /orders/{order_id}` — confirm `status` is `created` or `paid`
   - If `fulfilled` → order cannot be cancelled; handle as a business logic error in your flow
   - If already `cancelled` → treat as success; no further action needed
2. `DELETE /orders/{order_id}` — sets status to `cancelled`
   - Expect `204 No Content`; do not parse a response body

**Note:** Unlike `DELETE /customers`, cancelling an order is not permanent — the order record is retained with `status: cancelled`.

---

## 6. Recover a Failed Write

**When to use:** A POST or PATCH returned a network error or 5xx and you don't know if it succeeded.

For endpoints that **support idempotency** (`PATCH /customers/{id}`, `POST /orders`, `PATCH /orders/{id}`):
1. Reuse the exact same `Idempotency-Key` you generated before the original call
2. Retry the exact same request body — the server returns the cached result if it already succeeded
3. A 409 with `idempotency_conflict` in the `type` field means you changed the request body — use a new key and a new request

For `POST /customers` (no idempotency support):
1. `GET /customers?email=<email>&limit=1` — check if the customer was created
2. If found → use the existing `id`, do not retry the POST
3. If not found → retry the POST
