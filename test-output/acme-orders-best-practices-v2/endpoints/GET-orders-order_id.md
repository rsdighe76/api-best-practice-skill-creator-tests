# GET /orders/{order_id}

Read this file when: you are fetching a single order by ID or polling for a status change after a PATCH.

## The Working Request

```bash
curl "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

## Gotchas

- **Always include the full `ord_` prefix** — strip it and you'll get a 404.

## Order Status Values

| Status | Meaning |
|--------|---------|
| `created` | Placed, awaiting payment |
| `paid` | Payment confirmed |
| `fulfilled` | Shipped/delivered |
| `cancelled` | Cancelled |

## For Full Code Implementations

**Error handling:** See `shared/error-codes.md`. 404 → verify ID includes `ord_`.

**Timeout:** 10s. **Rate limit:** 600/min (read). **Retry:** 500ms initial, ×2, max 8s, 3 retries.

## What This Skill Validates

**Request-level:** ✓ `Authorization` with `orders:read` · ✓ `order_id` includes `ord_` prefix

**Code-level:** ✓ 404 handled separately · ✓ 10s timeout
