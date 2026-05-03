# GET /v1/orders

Read this file when: you are listing or filtering orders by customer, status, or other criteria and want to know how to paginate correctly.

## The Working Request

```bash
# List all orders for a specific customer
curl "https://api.acme.example/v1/orders?customer_id=cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A&limit=100" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
```

Filter by status:

```bash
curl "https://api.acme.example/v1/orders?status=paid&limit=100" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
```

## Gotchas

- **Default limit is 20.** Always pass `limit=100` for bulk operations to minimise round trips.
- **`status` filter is exact-match only — one value at a time.** You cannot query "not cancelled" or pass multiple statuses. If you need exclusion logic, filter client-side after fetching.
- **Recommended client-side cache: 15 seconds.** Shorter than the customers cache because order status changes more frequently. Do not cache longer than 15s in active order-processing flows.

## What Fails ❌

```bash
# Invalid status value
curl "https://api.acme.example/v1/orders?status=shipped" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
# → 400: status must be one of: created, paid, fulfilled, cancelled
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `limit` | integer 1–100 | No | Page size; defaults to 20 |
| `cursor` | string | No | Pagination cursor from previous response's `next_cursor` |
| `customer_id` | string | No | Filter by customer; use `cus_` prefix IDs |
| `status` | string | No | Filter by status: `created`, `paid`, `fulfilled`, `cancelled` |

## Response Shape

```json
{
  "data": [ /* array of Order objects */ ],
  "next_cursor": "cur_01HX9P...",
  "has_more": true
}
```

When `has_more` is `false` or `next_cursor` is absent, you have reached the last page.

## For Full Code Implementations

**Error handling:**
- For global error codes, retry rules, and error format: see `shared/error-codes.md`
- `400` on invalid `status` — use only `created`, `paid`, `fulfilled`, or `cancelled`

**Timeout:** 10 seconds.

**Rate limit:** 600 requests/minute (read bucket).

## What This Skill Validates

**Request-level checks:**
- ✓ `Authorization: Bearer` header present (requires `orders:read` scope)
- ✓ `limit` within 1–100 range if provided
- ✓ `status` is one of `created`, `paid`, `fulfilled`, `cancelled` if provided
- ✓ `customer_id` starts with `cus_` prefix if provided

**Code-level checks (full implementations only):**
- ✓ Timeout set to 10 seconds
- ✓ Pagination loop checks `next_cursor` or `has_more` — not response array length
- ✓ 429 handled with `retry_after_seconds` wait
