# Eval: PATCH /orders/{order_id} — Missing Idempotency Key

## Sample Request

```bash
curl -X PATCH "https://api.acme.example/v1/orders/ord_01HX9Q0M5Z6YB7R6C2D3E4F5G6" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "paid"}'
```

---

## Expected Findings

The skill MUST flag all of the following:

1. **Missing `Idempotency-Key` header**
   - Why: If this status update is retried without an idempotency key, the same transition may be applied twice or a conflicting state change may occur
   - Fix: Add `-H "Idempotency-Key: <uuid>"` — store the key before calling

---

## Pass Criteria

- [ ] Skill flags missing `Idempotency-Key` header on PATCH /orders
