# DELETE /v1/orders/{order_id}

Read this file when: you are cancelling an order and need to know which statuses allow cancellation, or what a 409 means here.

## The Working Request

```bash
curl -X DELETE "https://api.acme.example/v1/orders/ord_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
```

Expect `204 No Content` on success. The order record is retained with `status: cancelled` — it is NOT removed from the system.

## Gotchas

- **Cancellation is only possible from `created` or `paid` status.** A `fulfilled` order cannot be cancelled and returns 409. An already-`cancelled` order also returns 409 — check current status before calling.
- **This is a soft cancel, not a hard delete.** The order record persists with `status: cancelled`. Use `GET /orders/{order_id}` to confirm if needed.
- **No response body on success.** Do not attempt `response.json()` on a 204 — most HTTP clients will raise an error.

## What Fails ❌

```bash
# Cancelling a fulfilled order
curl -X DELETE "https://api.acme.example/v1/orders/ord_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
# → 409: order cannot be cancelled — current status is fulfilled
```

## Required Parameters

| Parameter | Location | Description |
|-----------|----------|-------------|
| `order_id` | path | Order ID — must start with `ord_` prefix |

## For Full Code Implementations

**Error handling:**
- For global error codes, retry rules, and error format: see `shared/error-codes.md`
- `409 order_already_fulfilled` — order cannot be cancelled; surface this as a business logic error in your flow, do not retry
- `409 order_already_cancelled` — treat as success in idempotent cancel flows
- `404` — order does not exist; treat as success in idempotent cleanup flows

**Timeout:** 15 seconds.

**Rate limit:** 60 requests/minute (delete bucket — lower limit than the standard write bucket).

## What This Skill Validates

**Request-level checks:**
- ✓ `Authorization: Bearer` header present (requires `orders:write` scope)
- ✓ `order_id` path parameter starts with `ord_` prefix

**Code-level checks (full implementations only):**
- ✓ Timeout set to 15 seconds
- ✓ 204 response handled — no attempt to parse response body
- ✓ Current order status confirmed with GET before attempting cancellation
- ✓ `409 order_already_fulfilled` handled as a business logic error — not retried
- ✓ `409 order_already_cancelled` and 404 treated as success in idempotent flows
- ✓ 429 handled with `retry_after_seconds` wait
