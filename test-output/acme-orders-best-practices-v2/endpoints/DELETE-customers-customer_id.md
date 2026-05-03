# DELETE /customers/{customer_id}

Read this file when: you are deleting a customer and need to understand the prerequisites, the irreversibility, and how to handle a 409.

## The Working Request

```bash
curl -X DELETE "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

Expect `204 No Content` — do not parse a response body.

## Gotchas

- **Permanent and irreversible** — there is no undo. Confirm the correct ID before calling.
- **Cancel open orders first** — 409 if the customer has active orders. Paginate `GET /orders?customer_id=<id>&status=created` and `status=paid`, cancel each, then delete.
- **Rate limit is 60/min** — lower than other writes; bulk deletion will hit this quickly.

## What Fails ❌

```bash
# No prerequisite check — will 409 if customer has open orders
curl -X DELETE "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_TOKEN"
```

## For Full Code Implementations

**Error handling:** See `shared/error-codes.md`. 409 → cancel open orders, retry. 404 → don't treat as success.

**Safe deletion sequence:** See `shared/workflows.md` → Workflow 5.

**Timeout:** 30s. **Rate limit:** 60/min (delete). **Retry:** 2s initial, max 1 retry.

## What This Skill Validates

**Request-level:** ✓ `Authorization` with `customers:write` · ✓ `customer_id` includes `cus_` prefix

**Code-level:** ✓ Open orders cancelled before deletion · ✓ 204 handled (no body) · ✓ 409 handled with recovery · ✓ Max 1 retry
