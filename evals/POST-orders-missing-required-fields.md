# Eval: POST /orders — Missing Required Fields

## Sample Request

```bash
curl -X POST "https://api.acme.example/v1/orders" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  -H "Idempotency-Key: 7b2f3d1a-9b8a-4f21-8d7a-12a3b4c5d6e7" \
  -H "Content-Type: application/json" \
  -d '{
    "items": []
  }'
```

---

## Expected Findings

The skill MUST flag all of the following:

1. **Missing `customer_id`**
   - Why: `customer_id` is always required — the order cannot be created without it
   - Fix: Add `"customer_id": "cus_..."` to the request body

2. **Empty `items` array**
   - Why: At least one item is required (`minItems: 1`)
   - Fix: Add at least one item with `sku`, `quantity`, and `unit_amount`

---

## Pass Criteria

- [ ] Skill flags missing `customer_id`
- [ ] Skill flags empty `items` array
