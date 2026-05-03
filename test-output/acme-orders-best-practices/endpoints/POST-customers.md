# POST /customers — Create a Customer

## What You Need to Know

**Creates a new customer record. This endpoint is NOT idempotent — if you retry on failure, you may create duplicate customers. Use `external_ref` deduplication on your side for safe retries.**

### Quick Checklist

When you call this endpoint, make sure you:
1. Include `Authorization: Bearer <token>` with `customers:write` scope
2. Include `name` and `email` in the request body
3. Include `company_name` if `account_type = "business"`
4. Do NOT include an `Idempotency-Key` header — this endpoint does not support it

### Example: Good Request

```bash
curl -X POST "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane.doe@example.com"
  }'
```

### Example: Common Mistakes ❌

```bash
# Missing email — will return 400
curl -X POST "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -d '{"name": "Jane Doe"}'

# Missing company_name for business account — will return 400
curl -X POST "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -d '{"name": "Acme Corp", "email": "billing@acme.com", "account_type": "business"}'
```

### Required Fields

**Always required:**
- `name` (string, min 1 char) — full name of the customer
- `email` (string, valid email format)

**Context-dependent:**
- `company_name` (string) — required when `account_type = "business"`

### For Full Code Implementations

**Error handling:**
- See `shared/error-codes.md` for global error codes and retry rules
- Endpoint-specific errors:
  - `400` with `field: email, code: invalid_format` — email is malformed
  - `400` with `field: company_name` — missing for business account type

**Timeouts:** Set a **30-second** timeout for this write operation.

**Rate limit:** 120 requests/minute (write bucket). Check `X-RateLimit-Remaining`.

**Safe retries:** This endpoint is NOT idempotent. If a request fails mid-flight, do NOT blindly retry — you may create a duplicate. Instead, call `GET /customers?email=<email>` first to check if the customer already exists.

### What This Skill Validates

**Request-level:**
- ✓ `Authorization` header present with `customers:write` scope
- ✓ `name` included
- ✓ `email` included and properly formatted
- ✓ `company_name` included when `account_type = "business"`

**Code-level:**
- ✓ No idempotency key being sent (not supported)
- ✓ Duplicate-customer check before retry
- ✓ 30-second timeout set
- ✓ Error handling branches on 400 vs 5xx
