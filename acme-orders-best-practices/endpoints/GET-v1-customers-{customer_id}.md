# GET /v1/customers/{customer_id}

Read this file when: you are fetching a single customer by ID and want to know what errors to expect.

## The Working Request

```bash
curl "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
```

## Gotchas

- **404 means the ID doesn't exist — don't retry it.** If you're getting a 404, check that you're using an `id` value from a previous create or list response, not a user-supplied string.
- **ID format is `cus_` prefixed.** Order IDs use `ord_`. Mixing them up returns 404, not 400.

## What Fails ❌

```bash
# Order ID used for a customer lookup
curl "https://api.acme.example/v1/customers/ord_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
# → 404: customer not found
```

## Required Parameters

| Parameter | Location | Description |
|-----------|----------|-------------|
| `customer_id` | path | Customer ID — must start with `cus_` prefix |

## For Full Code Implementations

**Error handling:**
- For global error codes, retry rules, and error format: see `shared/error-codes.md`
- `404` — customer does not exist; do not retry with the same ID

**Timeout:** 10 seconds.

**Rate limit:** 600 requests/minute (read bucket).

## What This Skill Validates

**Request-level checks:**
- ✓ `Authorization: Bearer` header present (requires `customers:read` scope)
- ✓ `customer_id` path parameter starts with `cus_` prefix

**Code-level checks (full implementations only):**
- ✓ Timeout set to 10 seconds
- ✓ 404 handled explicitly — not retried
- ✓ 429 handled with `retry_after_seconds` wait
