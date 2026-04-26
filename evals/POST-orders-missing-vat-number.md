# Eval: POST /orders — Missing VAT Number for EU Customer

## Sample Request

```bash
curl -X POST "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Idempotency-Key: 7b2f3d1a-9b8a-4f21-8d7a-12a3b4c5d6e7" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A",
    "billing_country": "DE",
    "items": [
      {"sku": "sku_anvil_001", "quantity": 1, "unit_amount": 1999}
    ]
  }'
```

---

## Expected Findings

The skill MUST flag all of the following:

1. **Missing `vat_number` for EU customer**
   - Why: `billing_country` is `DE` (Germany, an EU country) — `vat_number` is required for EU customers
   - Fix: Add `"vat_number": "DE123456789"` to the request body

---

## Pass Criteria

- [ ] Skill flags missing `vat_number` for EU customer (billing_country = DE)
