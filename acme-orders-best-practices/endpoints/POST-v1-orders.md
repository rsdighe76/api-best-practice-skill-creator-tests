# POST /v1/orders

Read this file when: you are creating a new order and want to know what fields are required, when context-dependent fields apply, and how to handle this safely with idempotency.

## The Working Request

```bash
# Generate and store the key BEFORE sending
IDEMPOTENCY_KEY=$(uuidgen)
# Write $IDEMPOTENCY_KEY to durable storage here before proceeding

curl -X POST "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Idempotency-Key: $IDEMPOTENCY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A",
    "items": [
      {
        "sku": "sku_anvil_001",
        "quantity": 2,
        "unit_amount": 1999
      }
    ]
  }'
```

## Gotchas

- **Always use an `Idempotency-Key` — and store it before the call.** Order creation is the highest-risk operation to duplicate. Generate a UUID, persist it to durable storage, then make the call. If your process crashes between sending and receiving, replay with the same key to recover the original result.
- **`amount_total` is computed server-side — do not send it.** The server calculates it from `items[].quantity * items[].unit_amount`. Including it causes a 400.
- **`customer_id` must reference an existing customer.** The API validates existence at create time. A deleted or non-existent customer returns 404, not 400.
- **Orders over $1,000 require `purchase_order_number`.** If the sum of `quantity × unit_amount` across all items exceeds 100,000 cents, you must include `purchase_order_number` or the request is rejected with 400. Compute this before submitting.
- **Items that require physical shipping need `shipping_address`.** If any item has `requires_shipping: true`, the top-level `shipping_address` object is required.

## What Fails ❌

```bash
# No Idempotency-Key — dangerous on a write
curl -X POST "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A", "items": [{"sku": "sku_anvil_001", "quantity": 1, "unit_amount": 1999}]}'
# → 400: Idempotency-Key header is required for POST /orders

# Sending amount_total (computed server-side)
curl -X POST "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A", "amount_total": 3998, "items": [{"sku": "sku_anvil_001", "quantity": 2, "unit_amount": 1999}]}'
# → 400: amount_total is computed server-side; do not include it in the request
```

## Required Fields

**Always required:**
- `customer_id` (string) — must reference an existing customer; use `cus_` prefix IDs
- `items` (array, minItems: 1) — at least one item
  - `items[].sku` (string, minLength: 1) — product SKU
  - `items[].quantity` (integer, min: 1) — number of units
  - `items[].unit_amount` (integer, min: 0) — price per unit in cents

**Context-dependent:**
- `purchase_order_number` (string) — required when the total order value (sum of `quantity × unit_amount` across all items) exceeds 100,000 cents ($1,000.00)
- `shipping_address` (object) — required when any item in `items` has `requires_shipping: true`
  - `shipping_address.line1` (string) — street address
  - `shipping_address.city` (string)
  - `shipping_address.country` (string, ISO 3166-1 alpha-2)
  - `shipping_address.postal_code` (string)

**Do NOT send:**
- `amount_total` — computed server-side from items
- `id`, `status`, `created_at`, `updated_at` — set server-side

## For Full Code Implementations

**Error handling:**
- For global error codes, retry rules, and error format: see `shared/error-codes.md`
- Endpoint-specific errors:
  - `400 idempotency_key_required` — add the `Idempotency-Key` header
  - `400 amount_total_not_allowed` — remove `amount_total` from the request body
  - `400 purchase_order_number_required` — total exceeds $1,000; include the field
  - `400 shipping_address_required` — one or more items require physical shipping
  - `404` — `customer_id` does not exist; verify the customer before creating the order
  - `409 idempotency_conflict` — same key reused with a different body; use a new key

**Timeout:** 30 seconds.

**Rate limit:** 120 requests/minute (write bucket).

## What This Skill Validates

**Request-level checks:**
- ✓ `Authorization: Bearer` header present (requires `orders:write` scope)
- ✓ `Idempotency-Key` header present, UUID v4 format (36 chars)
- ✓ `Content-Type: application/json` header present
- ✓ `customer_id` present and starts with `cus_` prefix
- ✓ `items` array present with at least one item
- ✓ Each item has `sku` (non-empty), `quantity` (≥1), and `unit_amount` (≥0)
- ✓ `purchase_order_number` present when total item value exceeds 100,000 cents
- ✓ `shipping_address` present when any item has `requires_shipping: true`
- ✓ `amount_total` NOT included in the request body

**Code-level checks (full implementations only):**
- ✓ Idempotency key generated and written to durable storage before the HTTP call
- ✓ Timeout set to 30 seconds
- ✓ 404 handled: verify customer exists before order creation in high-volume flows
- ✓ 409 handled: distinguish idempotency conflict (new key) from other conflicts
- ✓ On network error or 5xx, same idempotency key reused for the retry
- ✓ 429 handled with `retry_after_seconds` wait
