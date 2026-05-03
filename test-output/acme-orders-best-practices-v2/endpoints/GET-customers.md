# GET /customers

Read this file when: you are listing or searching customers, or checking if a customer exists by email before creating one.

## The Working Request

```bash
# Check if customer exists by email
curl -G "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  --data-urlencode "email=jane.doe@acmecorp.com" \
  --data-urlencode "limit=1"
```

## Gotchas

- **Single page is not the full list** — default page size is 20; always loop on `next_cursor`.
- **Use limit=100** — reduces round trips by 5× vs the default.
- **Results can be cached 30s** — don't call in a tight loop.

## What Fails ❌

```python
# Stops after 20 results — silently misses the rest
return GET("/customers")["data"]
```

## Parameters

| Parameter | Default | Max | Description |
|-----------|---------|-----|-------------|
| `limit` | 20 | 100 | Results per page |
| `cursor` | — | — | From previous `next_cursor` |
| `email` | — | — | Exact match filter |

## For Full Code Implementations

**Pagination:**
```python
cursor, results = None, []
while True:
    params = {"limit": 100}
    if cursor: params["cursor"] = cursor
    resp = GET("/customers", params=params)
    results.extend(resp["data"])
    cursor = resp.get("next_cursor")
    if not cursor: break
```

**Timeout:** 10s. **Rate limit:** 600/min (read). **Retry:** 500ms initial, ×2, max 8s, 3 retries.

## What This Skill Validates

**Request-level:** ✓ `Authorization` with `customers:read` scope

**Code-level:**
- ✓ Pagination loop — not assuming one page is complete
- ✓ `next_cursor` null-checked before stopping
- ✓ `limit=100` used
- ✓ 10s timeout set
