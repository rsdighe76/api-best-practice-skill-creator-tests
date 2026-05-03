# GET /orders

Read this file when: you are listing orders, filtering by customer or status, or checking for open orders before deleting a customer.

## The Working Request

```bash
curl -G "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  --data-urlencode "customer_id=cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  --data-urlencode "limit=100"
```

## Gotchas

- **Always paginate** — default page size is 20; customers with more than 20 orders are silently truncated.
- **Use limit=100** — 5× fewer requests vs the default.
- **Cache for 15s** — don't poll in a tight loop.

## What Fails ❌

```python
# Stops after first 20 — silently misses the rest
return GET("/orders", params={"customer_id": id})["data"]
```

## Parameters

| Parameter | Default | Max | Description |
|-----------|---------|-----|-------------|
| `limit` | 20 | 100 | Results per page |
| `cursor` | — | — | From previous `next_cursor` |
| `customer_id` | — | — | Filter by customer |
| `status` | — | — | `created`, `paid`, `fulfilled`, `cancelled` |

## For Full Code Implementations

```python
cursor, results = None, []
while True:
    params = {"limit": 100, "customer_id": customer_id}
    if cursor: params["cursor"] = cursor
    resp = GET("/orders", params=params)
    results.extend(resp["data"])
    cursor = resp.get("next_cursor")
    if not cursor: break
```

**Timeout:** 10s. **Rate limit:** 600/min (read). **Retry:** 500ms initial, ×2, max 8s, 3 retries.

## What This Skill Validates

**Request-level:** ✓ `Authorization` with `orders:read`

**Code-level:** ✓ Pagination loop · ✓ `next_cursor` checked · ✓ `limit=100` · ✓ 10s timeout
