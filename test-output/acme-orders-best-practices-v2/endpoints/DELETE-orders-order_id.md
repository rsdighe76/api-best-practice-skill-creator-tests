# DELETE /orders/{order_id}

Read this file when: you are cancelling an order and need to know which statuses allow cancellation and what response to expect.

## The Working Request

```bash
curl -X DELETE "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

Expect `204 No Content` — do not parse a response body.

## Gotchas

- **Logical cancellation, not hard delete** — status moves to `cancelled`; unlike DELETE /customers, this is not permanent.
- **Only cancellable from `created` or `paid`** — a `fulfilled` order cannot be cancelled; you'll get a 409.
- **204 means no body** — do not call `.json()` on the response.

## What Fails ❌

```bash
# Cancelling a fulfilled order — 409
curl -X DELETE "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN"
# ❌ Will fail if order is already fulfilled
```

## For Full Code Implementations

**Error handling:** See `shared/error-codes.md`. 409 → order not cancellable in current state. 404 → order not found.

**Timeout:** 30s. **Rate limit:** 60/min (delete). **Retry:** 2s initial, max 1 retry.

## What This Skill Validates

**Request-level:** ✓ `Authorization` with `orders:write` · ✓ `order_id` includes `ord_` prefix

**Code-level:** ✓ 204 handled (no body) · ✓ 409 not retried · ✓ max 1 retry
