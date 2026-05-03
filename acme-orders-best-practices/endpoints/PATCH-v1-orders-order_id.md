# PATCH /v1/orders/{order_id}

Read this file when: you are updating an order's status and need to know which transitions are valid, how to use idempotency safely, or what a 409 means.

## The Working Request

```bash
# Generate and store the key BEFORE sending
IDEMPOTENCY_KEY=$(uuidgen)
# Write $IDEMPOTENCY_KEY to durable storage before proceeding

curl -X PATCH "https://api.acme.example/v1/orders/ord_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Idempotency-Key: $IDEMPOTENCY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "paid"
  }'
```

## Gotchas

- **Status transitions are enforced server-side.** Only specific transitions are allowed (see table below). Attempting an invalid transition — e.g. moving a `fulfilled` order back to `paid` — returns 409. Always confirm current status with `GET /orders/{order_id}` before transitioning.
- **`fulfilled` and `cancelled` are terminal states.** Once an order reaches either state, no further transitions are possible.
- **Store the idempotency key before the call.** If a network failure occurs mid-flight, you need the original key to replay safely. Each distinct status transition requires its own unique key.
- **Do not include `items` in the body.** Line items are immutable after order creation.

## What Fails ❌

```bash
# Invalid transition: fulfilled → paid
curl -X PATCH "https://api.acme.example/v1/orders/ord_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{"status": "paid"}'
# → 409: invalid status transition from fulfilled to paid

# Missing Idempotency-Key
curl -X PATCH "https://api.acme.example/v1/orders/ord_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "paid"}'
# → 400: Idempotency-Key header is required for PATCH operations
```

## Valid Status Transitions

| From | To | Meaning |
|------|----|---------|
| `created` | `paid` | Payment received |
| `created` | `cancelled` | Cancel before payment |
| `paid` | `fulfilled` | Order shipped or delivered |
| `paid` | `cancelled` | Cancel after payment — triggers refund |
| `fulfilled` | — | Terminal; no further transitions allowed |
| `cancelled` | — | Terminal; no further transitions allowed |

## Required Fields

**Path parameter:**
- `order_id` — order ID, must start with `ord_` prefix

**Header:**
- `Idempotency-Key` — UUID v4, 36 characters; unique per transition; stored before the call

**Body (at least one required):**
- `status` (string) — target status; must be a valid transition from the current state

**Do NOT send:**
- `id`, `customer_id`, `amount_total`, `created_at`, `updated_at` — read-only
- `items` — line items are immutable after order creation

## For Full Code Implementations

**Error handling:**
- For global error codes, retry rules, and error format: see `shared/error-codes.md`
- `409 invalid_status_transition` — check current order status with GET before retrying; do not reuse the same key with a different target status
- `409 idempotency_conflict` — same key used with a different body; generate a new key for the new transition
- `404` — order not found; do not retry

**Timeout:** 30 seconds.

**Rate limit:** 120 requests/minute (write bucket).

## What This Skill Validates

**Request-level checks:**
- ✓ `Authorization: Bearer` header present (requires `orders:write` scope)
- ✓ `Idempotency-Key` header present, UUID v4 format (36 chars)
- ✓ `Content-Type: application/json` header present
- ✓ `status` value is a valid transition target (`paid`, `fulfilled`, or `cancelled`)
- ✓ `items` NOT included in the body

**Code-level checks (full implementations only):**
- ✓ Idempotency key generated and stored to durable storage before the HTTP call
- ✓ Current order status confirmed with GET before sending PATCH
- ✓ Timeout set to 30 seconds
- ✓ 409 handled: distinguish `invalid_status_transition` from `idempotency_conflict`
- ✓ On network error or 5xx, same idempotency key reused for the retry
- ✓ 429 handled with `retry_after_seconds` wait
