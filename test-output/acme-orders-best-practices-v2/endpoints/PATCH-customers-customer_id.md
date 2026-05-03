# PATCH /customers/{customer_id}

Read this file when: you are updating a customer's name or email and want to know the idempotency requirements and what errors to expect.

## The Working Request

```bash
curl -X PATCH "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Idempotency-Key: 7b2f3d1a-9b8a-4f21-8d7a-12a3b4c5d6e7" \
  -H "Content-Type: application/json" \
  -d '{"email": "jane.new@acmecorp.com"}'
```

## Gotchas

- **Persist the key before the call** — generate it and store it before calling the API. If the call fails, reuse the same key to retry safely.
- **Empty body returns 400** — at least one field required (`minProperties: 1`).
- **409 means key conflict** — generate a new key; retrying with the same key and different payload always 409s.

## What Fails ❌

```bash
# No idempotency key — unsafe to retry
curl -X PATCH "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -d '{"email": "jane.new@acmecorp.com"}'
```

## Required Fields

At least one of: `name` (string, min 1 char) or `email` (string, valid email).

## For Full Code Implementations

**Error handling:** See `shared/error-codes.md`. 409 → new key; 404 → customer not found.

**Timeout:** 30s. **Rate limit:** 120/min (write). **Retry:** 1s initial, ×2 + jitter, max 30s, 3 retries.

## What This Skill Validates

**Request-level:** ✓ `Authorization` with `customers:write` · ✓ `Idempotency-Key` present (8–128 chars) · ✓ At least one field in body

**Code-level:** ✓ Key persisted before call · ✓ 409 → new key generated · ✓ 30s timeout
