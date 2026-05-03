# PATCH /orders/{order_id} — Update an Order

## What You Need to Know

**Partially updates an order — typically used to advance the order lifecycle by updating `status`. Supports idempotency.**

### Quick Checklist

1. Include `Authorization: Bearer <token>` with `orders:write` scope
2. Include `Idempotency-Key` header for safe retries
3. Send only the field(s) you want to change (at least one required)
4. Use the full `ord_` prefixed order ID
5. Respect the valid status transitions

### Valid Status Transitions

| From | To | Meaning |
|------|----|---------|
| `created` | `paid` | Payment confirmed |
| `paid` | `fulfilled` | Order shipped/delivered |
| `created` or `paid` | `cancelled` | Order cancelled |

### About Idempotency

Always include an idempotency key:

```bash
-H "Idempotency-Key: <unique-uuid>"
```

Window is **24 hours**.

### Example: Good Request

```bash
# Mark an order as paid
curl -X PATCH "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Idempotency-Key: 7b2f3d1a-9b8a-4f21-8d7a-12a3b4c5d6e7" \
  -H "Content-Type: application/json" \
  -d '{"status": "paid"}'
```

### Example: Common Mistakes ❌

```bash
# No idempotency key — unsafe to retry a status change
curl -X PATCH "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -d '{"status": "paid"}'

# Empty body — 400 (minProperties: 1)
curl -X PATCH "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -d '{}'
```

### For Full Code Implementations

**Error handling:** See `shared/error-codes.md` for global error codes and retry rules.
- `400` — empty body or invalid status value
- `404` — order not found
- `409` — idempotency key reused with different payload; generate a new key

**Timeouts:** Set a **30-second** timeout.

**Rate limit:** 120 requests/minute (write bucket).

### What This Skill Validates

**Request-level:**
- ✓ `Authorization` header with `orders:write` scope
- ✓ `Idempotency-Key` header present (8–128 chars)
- ✓ At least one field in request body
- ✓ `status` value is one of: `created`, `paid`, `fulfilled`, `cancelled`

**Code-level:**
- ✓ 404 handled
- ✓ 409 handled — new key generated
- ✓ 30-second timeout set
