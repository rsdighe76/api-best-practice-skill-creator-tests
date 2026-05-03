# POST /orders — Create an Order

## What You Need to Know

**Creates a new order for an existing customer. Requires idempotency — always include an `Idempotency-Key` to prevent duplicate orders if a request fails mid-flight.**

### Quick Checklist

1. Include `Authorization: Bearer <token>` with `orders:write` scope
2. **Include `Idempotency-Key` header** — duplicate orders are costly
3. Include `customer_id` (must exist) and `items` array (at least one item)
4. Include `vat_number` if the customer is in an EU country
5. Do NOT include `amount_total` — it is computed server-side

### About Idempotency

Always include an idempotency key:

```bash
-H "Idempotency-Key: <unique-uuid>"
```

Window is **24 hours**. Store the key with your order record so you can safely retry with the same key if needed.

```python
import uuid
idempotency_key = str(uuid.uuid4())
# Store this key alongside your order record before calling the API
```

### Example: Good Request

```bash
curl -X POST "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Idempotency-Key: 7b2f3d1a-9b8a-4f21-8d7a-12a3b4c5d6e7" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A",
    "items": [
      {"sku": "sku_anvil_001", "quantity": 1, "unit_amount": 1999}
    ]
  }'
```

### Example: Common Mistakes ❌

```bash
# No idempotency key — risk of duplicate orders on retry
curl -X POST "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -d '{"customer_id": "cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A", "items": [...]}'

# Sending amount_total — will be ignored or cause 400
curl -X POST "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Idempotency-Key: abc123" \
  -d '{"customer_id": "cus_...", "items": [...], "amount_total": 1999}'
```

### Required Fields

**Always required:**
- `customer_id` (string) — must be an existing customer ID with `cus_` prefix
- `items` (array, min 1 item) — each item requires:
  - `sku` (string)
  - `quantity` (integer, min 1)
  - `unit_amount` (integer, min 0, in minor currency units e.g. cents)

**Context-dependent:**
- `vat_number` (string) — required when customer billing country is in the EU

**Do NOT send:**
- `amount_total` — computed server-side, ignored or rejected if sent

### For Full Code Implementations

**Error handling:** See `shared/error-codes.md` for global error codes and retry rules.
- `400` — missing required fields or invalid item data
- `404` — `customer_id` does not exist
- `409` — idempotency key reused with different payload; generate a new key

**Timeouts:** Set a **30-second** timeout.

**Rate limit:** 120 requests/minute (write bucket).

### What This Skill Validates

**Request-level:**
- ✓ `Authorization` header with `orders:write` scope
- ✓ `Idempotency-Key` header present (8–128 chars)
- ✓ `customer_id` present with `cus_` prefix
- ✓ `items` array present with at least one item
- ✓ Each item has `sku`, `quantity`, `unit_amount`
- ✓ `vat_number` present for EU customers
- ✓ `amount_total` NOT sent in request body

**Code-level:**
- ✓ Idempotency key stored before API call
- ✓ 404 handled (customer not found)
- ✓ 409 handled (key conflict — new key generated)
- ✓ 30-second timeout set
