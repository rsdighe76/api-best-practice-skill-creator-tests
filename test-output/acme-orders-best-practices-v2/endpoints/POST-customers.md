# POST /customers

Read this file when: you are creating a new customer and want to know what's required, why you must check before creating, and how to retry safely.

## The Working Request

```bash
curl -X POST "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "email": "jane.doe@acmecorp.com"}'
```

## Gotchas

- **NOT idempotent** — every call creates a new record. Always call `GET /customers?email=<email>` first; only POST if no match is found.
- **company_name required for business accounts** — if `account_type = "business"`, omitting it returns a 400.
- **No Idempotency-Key support** — use the check-then-create pattern for safe retries instead.

## What Fails ❌

```bash
# Retrying without checking first — creates a duplicate customer
curl -X POST "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -d '{"name": "Jane Doe", "email": "jane.doe@acmecorp.com"}'
```

## Required Fields

**Always required:** `name` (string, min 1 char), `email` (string, valid email)

**Context-dependent:** `company_name` (string) — required when `account_type = "business"`

## For Full Code Implementations

**Error handling:** See `shared/error-codes.md`. Safe retry: `GET /customers?email=<email>&limit=1` before POST.

**Timeout:** 30s. **Rate limit:** 120/min (write). **Retry:** 1s initial, ×2 + jitter, max 30s, 3 retries — but check for duplicate before each retry.

## What This Skill Validates

**Request-level:**
- ✓ `Authorization` header with `customers:write` scope
- ✓ `name` and `email` present; email is valid format
- ✓ `company_name` present when `account_type = "business"`

**Code-level:**
- ✓ Duplicate check (`GET /customers?email=`) before POST
- ✓ 30s timeout set
- ✓ 400 not retried
- ✓ Retry only on 429, 500, 502, 503
