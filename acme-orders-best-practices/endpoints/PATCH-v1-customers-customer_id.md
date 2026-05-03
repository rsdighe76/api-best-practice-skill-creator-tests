# PATCH /v1/customers/{customer_id}

Read this file when: you are updating customer fields and want to know how to use idempotency correctly or handle conflicts.

## The Working Request

```bash
# Generate and store the key before sending
IDEMPOTENCY_KEY="550e8400-e29b-41d4-a716-446655440000"

curl -X PATCH "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Idempotency-Key: $IDEMPOTENCY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane.new@acme-customer.com"
  }'
```

## Gotchas

- **PATCH is partial — only send fields you want to change.** Omitting a field leaves it unchanged. This is intentional; do not send the full object if you only want to update one field.
- **Generate and store the idempotency key before making the call.** If your process crashes after sending but before receiving a response, you need that key to replay the request safely. Generating it inline (e.g. `$(uuidgen)` in a shell one-liner) without storing it first loses the key.
- **Same key with a different body returns 409.** If you reuse an `Idempotency-Key` but change the request body, the API rejects with 409. Use a new key for intentionally different updates.

## What Fails ❌

```bash
# Missing Idempotency-Key
curl -X PATCH "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "jane.new@acme-customer.com"}'
# → 400: Idempotency-Key header is required for PATCH operations

# Same key, different body
curl -X PATCH "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{"email": "completely.different@example.com"}'
# → 409: idempotency key already used with a different request body
```

## Required Fields

**Path parameter:**
- `customer_id` — customer ID, must start with `cus_` prefix

**Header:**
- `Idempotency-Key` — UUID v4, 36 characters; unique per logical update operation; store it before the call

**Body (all optional, but at least one must be present):**
- `name` (string) — updated full name
- `email` (string, email format) — updated email; must still be globally unique
- `company_name` (string) — updated company name
- `vat_number` (string) — updated VAT number

**Do NOT send:**
- `id`, `created_at`, `updated_at` — read-only, ignored or rejected

## For Full Code Implementations

**Error handling:**
- For global error codes, retry rules, and error format: see `shared/error-codes.md`
- `409 idempotency_conflict` — same key with a different body; generate a new key for the new update
- `404` — customer does not exist; do not retry

**Timeout:** 30 seconds.

**Rate limit:** 120 requests/minute (write bucket).

## What This Skill Validates

**Request-level checks:**
- ✓ `Authorization: Bearer` header present (requires `customers:write` scope)
- ✓ `Idempotency-Key` header present, UUID v4 format (36 chars)
- ✓ `Content-Type: application/json` header present
- ✓ At least one field included in the body

**Code-level checks (full implementations only):**
- ✓ Idempotency key generated and stored to durable storage before the HTTP call
- ✓ Timeout set to 30 seconds
- ✓ 409 handled: distinguish `idempotency_conflict` (new key needed) from other conflicts
- ✓ On network error or 5xx, same key reused for the retry
- ✓ 429 handled with `retry_after_seconds` wait
