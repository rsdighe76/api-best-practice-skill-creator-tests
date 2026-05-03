# DELETE /v1/customers/{customer_id}

Read this file when: you are permanently deleting a customer and need to know what prerequisites to check first.

## The Working Request

```bash
curl -X DELETE "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
```

Expect `204 No Content` on success. Do not attempt to parse a response body.

## Gotchas

- **Irreversible.** There is no undo. The customer record is permanently removed.
- **Outstanding orders block deletion.** If the customer has any orders in `created` or `paid` status, the API returns 409. Cancel those orders first. Orders in `fulfilled` or `cancelled` status do not block deletion.
- **No response body on success.** A `204` means it worked. Calling `response.json()` on a 204 will raise an error in most HTTP clients.

## What Fails ❌

```bash
# Customer with open orders
curl -X DELETE "https://api.acme.example/v1/customers/cus_01HX9P2C7YQ2GQ7P9R8F2H2Z7A" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
# → 409: customer has open orders; cancel all created and paid orders before deleting
```

## Required Parameters

| Parameter | Location | Description |
|-----------|----------|-------------|
| `customer_id` | path | Customer ID — must start with `cus_` prefix |

## For Full Code Implementations

**Error handling:**
- For global error codes, retry rules, and error format: see `shared/error-codes.md`
- `409 has_open_orders` — cancel orders with status `created` or `paid` before retrying; see `shared/workflows.md` workflow 4
- `404` — customer already deleted or never existed; treat as success in idempotent cleanup flows

**Timeout:** 15 seconds.

**Rate limit:** 60 requests/minute (delete bucket — lower limit than the standard write bucket).

## What This Skill Validates

**Request-level checks:**
- ✓ `Authorization: Bearer` header present (requires `customers:write` scope)
- ✓ `customer_id` path parameter starts with `cus_` prefix

**Code-level checks (full implementations only):**
- ✓ Timeout set to 15 seconds
- ✓ 204 response handled — no attempt to parse response body
- ✓ 409 handled — open orders cancelled before retrying delete
- ✓ 404 treated as success in idempotent cleanup flows
- ✓ Customer ID logged before calling (operation is irreversible)
