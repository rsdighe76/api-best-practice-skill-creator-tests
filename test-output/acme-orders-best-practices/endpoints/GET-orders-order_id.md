# GET /orders/{order_id} — Retrieve an Order

## What You Need to Know

**Fetches a single order by ID. Simple read — use this to check order status after creation or updates.**

### Quick Checklist

1. Include `Authorization: Bearer <token>` with `orders:read` scope
2. Use the full `ord_` prefixed order ID
3. Handle 404 explicitly — the order may not exist

### Example: Good Request

```bash
curl "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

### Example: Common Mistakes ❌

```bash
# Stripped prefix — will return 404
curl "https://api.acme.example/v1/orders/01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

### Response: Order Status Values

| Status | Meaning |
|--------|---------|
| `created` | Order placed, awaiting payment |
| `paid` | Payment confirmed |
| `fulfilled` | Order shipped/delivered |
| `cancelled` | Order cancelled |

### For Full Code Implementations

**Error handling:** See `shared/error-codes.md` for global error codes and retry rules.
- `404` — order ID does not exist; verify the ID and prefix.

**Timeouts:** Set a **10-second** timeout.

**Rate limit:** 600 requests/minute (read bucket).

### What This Skill Validates

**Request-level:**
- ✓ `Authorization` header with `orders:read` scope
- ✓ `order_id` includes `ord_` prefix

**Code-level:**
- ✓ 404 handled separately from 5xx
- ✓ 10-second timeout set
