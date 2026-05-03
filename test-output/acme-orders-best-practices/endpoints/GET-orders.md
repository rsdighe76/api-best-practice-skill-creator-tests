# GET /orders — List Orders

## What You Need to Know

**Returns a paginated list of orders. Cursor-based pagination — always check `next_cursor`. Results can be filtered by customer or status.**

### Quick Checklist

1. Include `Authorization: Bearer <token>` with `orders:read` scope
2. Paginate through all results using `next_cursor`
3. Use `customer_id` filter to scope to a specific customer's orders
4. Use `status` filter to narrow results (created, paid, fulfilled, cancelled)

### Example: Good Request

```bash
# List all orders for a customer
curl -G "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  --data-urlencode "customer_id=cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  --data-urlencode "limit=100"

# Next page
curl -G "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  --data-urlencode "cursor=cur_01HX9R1ABCDEFGHJKL" \
  --data-urlencode "limit=100"
```

### Parameters

| Parameter | Required | Default | Max | Description |
|-----------|:--------:|---------|-----|-------------|
| `limit` | No | 20 | 100 | Results per page |
| `cursor` | No | — | — | Cursor from previous `next_cursor` |
| `customer_id` | No | — | — | Filter by customer |
| `status` | No | — | — | Filter by status: `created`, `paid`, `fulfilled`, `cancelled` |

### Pagination Pattern

```python
cursor = None
all_orders = []

while True:
    params = {"limit": 100, "customer_id": customer_id}
    if cursor:
        params["cursor"] = cursor
    response = get("/orders", params=params)
    all_orders.extend(response["data"])
    cursor = response.get("next_cursor")
    if not cursor:
        break
```

### For Full Code Implementations

**Error handling:** See `shared/error-codes.md` for global error codes and retry rules.

**Timeouts:** Set a **10-second** timeout.

**Rate limit:** 600 requests/minute (read bucket).

**Caching:** Results can be cached for up to 15 seconds.

### What This Skill Validates

**Request-level:**
- ✓ `Authorization` header with `orders:read` scope

**Code-level:**
- ✓ Pagination loop — not assuming single page is complete
- ✓ `next_cursor` null-check before stopping
- ✓ 10-second timeout set
