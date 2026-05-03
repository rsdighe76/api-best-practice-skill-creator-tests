# GET /v1/customers

Read this file when: you are listing or searching customers and want to know how to filter, paginate, or avoid burning your rate limit.

## The Working Request

```bash
# List all customers, maximum page size
curl "https://api.acme.example/v1/customers?limit=100" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
```

Filter by email (exact match):

```bash
curl "https://api.acme.example/v1/customers?email=jane.doe%40acme-customer.com&limit=1" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
```

## Gotchas

- **Default limit is 20.** For bulk operations, always pass `limit=100` — otherwise you'll make 5× more requests than necessary for large datasets.
- **Check `next_cursor` to detect more pages, not the array length.** A page with fewer than `limit` items does not mean you're on the last page — always check `next_cursor` or `has_more`.
- **`email` filter is exact-match only.** Partial matches and wildcards are not supported. URL-encode the `@` sign as `%40`.
- **Recommended client-side cache: 30 seconds.** This endpoint is marked with a 30s TTL hint. Cache responses locally when iterating in bulk to avoid redundant calls.

## What Fails ❌

```bash
# limit out of range
curl "https://api.acme.example/v1/customers?limit=500" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
# → 400: limit must be between 1 and 100

# Missing scope
curl "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ORDERS_ONLY_TOKEN"
# → 403: missing customers:read scope
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `limit` | integer 1–100 | No | Page size; defaults to 20. Use 100 for bulk operations. |
| `cursor` | string | No | Pagination cursor from previous response's `next_cursor` |
| `email` | string | No | Filter by exact email address; URL-encode special characters |

## Response Shape

```json
{
  "data": [ /* array of Customer objects */ ],
  "next_cursor": "cur_01HX9P...",
  "has_more": true
}
```

When `has_more` is `false` or `next_cursor` is absent, you have reached the last page.

## For Full Code Implementations

**Error handling:**
- For global error codes, retry rules, and error format: see `shared/error-codes.md`
- `400` on `limit` out of range — clamp to 1–100

**Timeout:** 10 seconds.

**Rate limit:** 600 requests/minute (read bucket).

## What This Skill Validates

**Request-level checks:**
- ✓ `Authorization: Bearer` header present (requires `customers:read` scope)
- ✓ `limit` within 1–100 range if provided
- ✓ `cursor` passed as query parameter, not in the request body

**Code-level checks (full implementations only):**
- ✓ Timeout set to 10 seconds
- ✓ Pagination loop checks `next_cursor` or `has_more` — not response array length
- ✓ 429 handled with `retry_after_seconds` wait
