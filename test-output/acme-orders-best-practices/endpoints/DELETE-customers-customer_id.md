# DELETE /customers/{customer_id} — Delete a Customer

## What You Need to Know

**⚠️ PERMANENT — this deletion is irreversible. There is no undo. The customer record and all associated data will be permanently removed.**

### Quick Checklist

1. Include `Authorization: Bearer <token>` with `customers:write` scope
2. Confirm you have the correct `customer_id` — deletion cannot be undone
3. Consider checking for active orders on this customer before deleting
4. Expect 204 (no response body) on success

### Example: Good Request

```bash
curl -X DELETE "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

### Example: Common Mistakes ❌

```bash
# Looping over a list and deleting in bulk without verification
# This can permanently destroy data with no recovery path
for id in "${customer_ids[@]}"; do
  curl -X DELETE "https://api.acme.example/v1/customers/$id" \
    -H "Authorization: Bearer $ACME_TOKEN"
done
# ❌ No confirmation step — irreversible at scale
```

### For Full Code Implementations

**Error handling:** See `shared/error-codes.md` for global error codes and retry rules.
- `404` — customer not found; do not treat as success
- `409` — customer has a dependency that prevents deletion (e.g., open orders)
- Successful deletion returns `204 No Content` — do not attempt to parse a response body

**Timeouts:** Set a **30-second** timeout.

**Rate limit:** 60 requests/minute (delete bucket — lower than other write operations).

### What This Skill Validates

**Request-level:**
- ✓ `Authorization` header present with `customers:write` scope
- ✓ `customer_id` includes `cus_` prefix

**Code-level:**
- ✓ 204 response handled (no body parsing)
- ✓ 409 handled — not retried
- ✓ 404 handled — not silently ignored
- ✓ 30-second timeout set
- ✓ No bulk-delete loop without explicit confirmation step
