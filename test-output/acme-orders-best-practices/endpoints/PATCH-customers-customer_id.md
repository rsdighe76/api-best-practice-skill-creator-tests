# PATCH /customers/{customer_id} — Update a Customer

## What You Need to Know

**Partially updates a customer. Only fields you send are changed — omitted fields are untouched. Supports idempotency.**

### Quick Checklist

1. Include `Authorization: Bearer <token>` with `customers:write` scope
2. Include `Idempotency-Key` header for safe retries
3. Send only the fields you want to change (at least one field required)
4. Use the full `cus_` prefixed customer ID

### About Idempotency

This endpoint supports idempotency — always include a key:

```bash
-H "Idempotency-Key: <unique-uuid>"
```

Window is **24 hours**. If you reuse the same key with a different payload within 24 hours, you'll get a 409.

Generate a key per operation:
```python
import uuid
idempotency_key = str(uuid.uuid4())
```

### Example: Good Request

```bash
curl -X PATCH "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Idempotency-Key: 7b2f3d1a-9b8a-4f21-8d7a-12a3b4c5d6e7" \
  -H "Content-Type: application/json" \
  -d '{"email": "jane.new@example.com"}'
```

### Example: Common Mistakes ❌

```bash
# No idempotency key — unsafe to retry
curl -X PATCH "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -d '{"email": "jane.new@example.com"}'

# Empty body — will return 400 (minProperties: 1)
curl -X PATCH "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -d '{}'
```

### Required Fields

At least one of:
- `name` (string, min 1 char)
- `email` (string, valid email format)

### For Full Code Implementations

**Error handling:** See `shared/error-codes.md` for global error codes and retry rules.
- `400` — empty body or invalid field value
- `404` — customer not found
- `409` — idempotency key reused with different payload; generate a new key

**Timeouts:** Set a **30-second** timeout.

**Rate limit:** 120 requests/minute (write bucket).

### What This Skill Validates

**Request-level:**
- ✓ `Authorization` header present with `customers:write` scope
- ✓ `Idempotency-Key` header present (8–128 chars)
- ✓ At least one field in the request body

**Code-level:**
- ✓ 409 handled — new key generated on conflict
- ✓ 404 handled separately
- ✓ 30-second timeout set
