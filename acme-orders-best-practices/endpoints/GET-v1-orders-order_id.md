# GET /v1/orders/{order_id}

Read this file when: you are fetching a single order by ID to check its current status or confirm a state transition succeeded.

## The Working Request

```bash
curl "https://api.acme.example/v1/orders/ord_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
```

## Gotchas

- **Order IDs use `ord_` prefix.** Customer IDs use `cus_`. Mixing them up returns 404, not a helpful error.
- **Use this to confirm status after a PATCH.** The PATCH /orders response returns the updated order, but if you need to poll for state in an async or webhook-driven flow, this is the endpoint to call.

## What Fails ❌

```bash
# Customer ID used in place of an order ID
curl "https://api.acme.example/v1/orders/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
# → 404: order not found
```

## Required Parameters

| Parameter | Location | Description |
|-----------|----------|-------------|
| `order_id` | path | Order ID — must start with `ord_` prefix |

## For Full Code Implementations

**Error handling:**
- For global error codes, retry rules, and error format: see `shared/error-codes.md`
- `404` — order does not exist; do not retry with the same ID

**Timeout:** 10 seconds.

**Rate limit:** 600 requests/minute (read bucket).

## What This Skill Validates

**Request-level checks:**
- ✓ `Authorization: Bearer` header present (requires `orders:read` scope)
- ✓ `order_id` path parameter starts with `ord_` prefix

**Code-level checks (full implementations only):**
- ✓ Timeout set to 10 seconds
- ✓ 404 handled explicitly — not retried
- ✓ 429 handled with `retry_after_seconds` wait
