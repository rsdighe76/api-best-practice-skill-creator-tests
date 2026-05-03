# GET /customers — List Customers

## What You Need to Know

**Returns a paginated list of customers. Cursor-based pagination — always check `next_cursor` to fetch all pages.**

### Quick Checklist

When you call this endpoint, make sure you:
1. Include `Authorization: Bearer <token>` with `customers:read` scope
2. Use `next_cursor` to paginate through all results — don't assume one page is everything
3. Respect the recommended cache TTL of 30 seconds if caching responses

### Example: Good Request

```bash
# First page
curl -G "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  --data-urlencode "limit=20"

# Next page using cursor from previous response
curl -G "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  --data-urlencode "cursor=cur_01HX9R1ABCDEFGHJKL" \
  --data-urlencode "limit=20"
```

### Example: Common Mistakes ❌

```bash
# Assuming one page contains all customers — will miss records
curl "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_TOKEN"
# ❌ No pagination loop — stops after first 20 results
```

### Parameters

| Parameter | Required | Default | Max | Description |
|-----------|:--------:|---------|-----|-------------|
| `limit` | No | 20 | 100 | Number of results per page |
| `cursor` | No | — | — | Opaque cursor from previous response's `next_cursor` |
| `email` | No | — | — | Filter by exact email match |

### Pagination Pattern

```python
cursor = None
all_customers = []

while True:
    params = {"limit": 100}
    if cursor:
        params["cursor"] = cursor
    response = get("/customers", params=params)
    all_customers.extend(response["data"])
    cursor = response.get("next_cursor")
    if not cursor:
        break
```

### For Full Code Implementations

**Error handling:** See `shared/error-codes.md` for global error codes and retry rules.

**Timeouts:** Set a **10-second** timeout for this read operation.

**Rate limit:** 600 requests/minute (read bucket). Check `X-RateLimit-Remaining`.

**Caching:** Results can be cached for up to 30 seconds safely.

### What This Skill Validates

**Request-level:**
- ✓ `Authorization` header present with `customers:read` scope

**Code-level:**
- ✓ Pagination loop implemented — not assuming single page
- ✓ `next_cursor` checked before stopping
- ✓ 10-second timeout set
