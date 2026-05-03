# PATCH /orders/{order_id}

Read this file when: you are advancing an order's status and need to know the valid transitions, idempotency requirements, and what to check before patching.

## The Working Request

```bash
curl -X PATCH "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Idempotency-Key: 7b2f3d1a-9b8a-4f21-8d7a-12a3b4c5d6e7" \
  -H "Content-Type: application/json" \
  -d '{"status": "paid"}'
```

## Gotchas

- **Check current status first** — always `GET /orders/{id}` before patching. If already at target, skip the PATCH.
- **Cannot skip states** — `created → fulfilled` is rejected; must go `created → paid → fulfilled`.
- **Persist the key before the call** — reuse on retry; server returns cached result if transition already happened.

## Valid Transitions

| From | To | When |
|------|----|------|
| `created` | `paid` | Payment confirmed |
| `paid` | `fulfilled` | Shipped |
| `created` or `paid` | `cancelled` | Cancelled |

## What Fails ❌

```bash
# No idempotency key — unsafe to retry a status change
curl -X PATCH "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -d '{"status": "paid"}'
```

## For Full Code Implementations

**Error handling:** See `shared/error-codes.md`. 409 → new key. 400 → invalid status or empty body.

**Timeout:** 30s. **Rate limit:** 120/min (write). **Retry:** 1s initial, ×2 + jitter, max 30s, 3 retries.

## What This Skill Validates

**Request-level:** ✓ `Authorization` with `orders:write` · ✓ `Idempotency-Key` (8–128 chars) · ✓ valid `status` value · ✓ at least one field in body

**Code-level:** ✓ `GET` before `PATCH` · ✓ key persisted before call · ✓ state machine respected · ✓ 409 → new key · ✓ 30s timeout
