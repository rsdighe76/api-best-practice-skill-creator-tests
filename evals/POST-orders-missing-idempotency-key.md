# Eval: POST /orders — Missing Idempotency Key

## Sample Request

```bash
curl -X POST "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A",
    "items": [
      {"sku": "sku_anvil_001", "quantity": 2, "unit_amount": 1999}
    ]
  }'
```

---

## Expected Findings

The skill MUST flag all of the following:

1. **Missing `Idempotency-Key` header**
   - Why: If this request fails mid-flight and is retried, a duplicate order will be created
   - Fix: Add `-H "Idempotency-Key: <uuid>"` and store the key before calling the API

---

## Pass Criteria

- [ ] Skill flags missing `Idempotency-Key` header
