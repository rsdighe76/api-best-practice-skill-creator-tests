# DELETE /orders/{order_id} — Cancel an Order

## What You Need to Know

**Cancels an order. This is a logical cancellation — the order status moves to `cancelled`. Unlike customer deletion, this is NOT irreversible; you can place a new order if needed.**

### Quick Checklist

1. Include `Authorization: Bearer <token>` with `orders:write` scope
2. Use the full `ord_` prefixed order ID
3. Only orders in `created` or `paid` status can be cancelled
4. Expect 204 (no response body) on success

### Example: Good Request

```bash
curl -X DELETE "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

### Example: Common Mistakes ❌

```bash
# Trying to cancel an already-fulfilled order — will return 409
curl -X DELETE "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN"
# ❌ If order is already fulfilled, cancellation is not allowed
```

### For Full Code Implementations

**Error handling:** See `shared/error-codes.md` for global error codes and retry rules.
- `404` — order not found
- `409` — order cannot be cancelled in its current status (e.g., already `fulfilled`)
- Successful cancellation returns `204 No Content` — do not attempt to parse a response body

**Timeouts:** Set a **30-second** timeout.

**Rate limit:** 60 requests/minute (delete bucket).

### What This Skill Validates

**Request-level:**
- ✓ `Authorization` header with `orders:write` scope
- ✓ `order_id` includes `ord_` prefix

**Code-level:**
- ✓ 204 handled (no body parsing)
- ✓ 409 handled — not retried
- ✓ 404 handled — not silently ignored
- ✓ 30-second timeout set
