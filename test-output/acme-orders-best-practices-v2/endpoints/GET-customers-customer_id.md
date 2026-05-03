# GET /customers/{customer_id}

Read this file when: you are fetching a single customer by ID.

## The Working Request

```bash
curl "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

## Gotchas

- **Always include the full `cus_` prefix** — strip it and you'll get a 404.

## What Fails ❌

```bash
# Missing prefix — 404
curl "https://api.acme.example/v1/customers/01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

## For Full Code Implementations

**Error handling:** See `shared/error-codes.md`. 404 means ID doesn't exist — don't retry.

**Timeout:** 10s. **Rate limit:** 600/min (read). **Retry:** 500ms initial, ×2, max 8s, 3 retries.

## What This Skill Validates

**Request-level:** ✓ `Authorization` with `customers:read` · ✓ `customer_id` includes `cus_` prefix

**Code-level:** ✓ 404 handled separately · ✓ 10s timeout
