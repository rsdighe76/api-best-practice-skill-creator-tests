# GET /customers/{customer_id} — Retrieve a Customer

## What You Need to Know

**Fetches a single customer by ID. Simple read — no idempotency or special headers needed.**

### Quick Checklist

1. Include `Authorization: Bearer <token>` with `customers:read` scope
2. Use the full customer ID including the `cus_` prefix
3. Handle 404 explicitly — the customer may not exist

### Example: Good Request

```bash
curl "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

### Example: Common Mistakes ❌

```bash
# Stripped prefix — will return 404
curl "https://api.acme.example/v1/customers/01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

### For Full Code Implementations

**Error handling:** See `shared/error-codes.md` for global error codes and retry rules.
- Endpoint-specific: `404` means the customer ID does not exist — do not retry, verify the ID.

**Timeouts:** Set a **10-second** timeout.

**Rate limit:** 600 requests/minute (read bucket).

### What This Skill Validates

**Request-level:**
- ✓ `Authorization` header present with `customers:read` scope
- ✓ `customer_id` includes `cus_` prefix

**Code-level:**
- ✓ 404 handled separately from 5xx
- ✓ 10-second timeout set
