# POST /orders

Read this file when: you are creating an order and want to know what's required, how to prevent duplicates with idempotency, and which context-dependent fields to include.

## The Working Request

```bash
curl -X POST "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Idempotency-Key: 7b2f3d1a-9b8a-4f21-8d7a-12a3b4c5d6e7" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A",
    "items": [{"sku": "sku_anvil_001", "quantity": 1, "unit_amount": 1999}]
  }'
```

## Gotchas

- **Persist the Idempotency-Key before the call** — if the process crashes mid-flight, you need that key to retry without creating a duplicate order.
- **amount_total is computed server-side** — sending it causes a 400.
- **vat_number required for EU customers** — if `billing_country` is in the EU, include it or the request is rejected.
- **unit_amount is in minor currency units** — cents for USD; `1999` = $19.99.

## What Fails ❌

```bash
# No idempotency key — duplicate order risk on retry
curl -X POST "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -d '{"customer_id": "cus_...", "items": [...]}'

# Sending amount_total — 400
curl -X POST "https://api.acme.example/v1/orders" \
  -H "Idempotency-Key: abc" \
  -d '{"customer_id": "cus_...", "items": [...], "amount_total": 1999}'
```

## Required Fields

**Always required:** `customer_id` (string, `cus_` prefix), `items[]` (min 1, each needs `sku`, `quantity`, `unit_amount`)

**Context-dependent:** `vat_number` (string) — required when `billing_country` is in EU

**Do NOT send:** `amount_total` — computed server-side

## For Full Code Implementations

**Error handling:** See `shared/error-codes.md`. 404 → customer not found. 409 → new key.

**Timeout:** 30s. **Rate limit:** 120/min (write). **Retry:** 1s initial, ×2 + jitter, max 30s, 3 retries.

## What This Skill Validates

**Request-level:** ✓ `Authorization` with `orders:write` · ✓ `Idempotency-Key` (8–128 chars) · ✓ `customer_id` with `cus_` prefix · ✓ `items[]` with at least one item · ✓ `vat_number` for EU · ✓ `amount_total` NOT sent

**Code-level:** ✓ Key persisted before call · ✓ 404 handled · ✓ 409 → new key · ✓ 30s timeout
