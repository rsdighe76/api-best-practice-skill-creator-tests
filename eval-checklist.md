# Eval Checklist — ACME Orders API Skill

Run the skill creator with `fixtures/acme-orders-openapi.yaml` and check the output against this list.
Generated files should land in `test-output/acme-orders-best-practices/`.

---

## Structure

- [ ] `SKILL.md` exists at the root
- [ ] `shared/error-codes.md` exists
- [ ] `endpoints/` directory exists
- [ ] Exactly 8 endpoint files exist (one per operation):
  - [ ] `POST-customers.md`
  - [ ] `GET-customers.md`
  - [ ] `GET-customers-{customer_id}.md`
  - [ ] `PATCH-customers-{customer_id}.md`
  - [ ] `DELETE-customers-{customer_id}.md`
  - [ ] `POST-orders.md`
  - [ ] `GET-orders.md`
  - [ ] `GET-orders-{order_id}.md`
  - [ ] `PATCH-orders-{order_id}.md`
  - [ ] `DELETE-orders-{order_id}.md`

---

## SKILL.md

- [ ] Frontmatter has `name` and `description`
- [ ] Description mentions ACME Orders API (not a generic placeholder)
- [ ] No `example.com` URLs — all URLs use `api.acme.example`
- [ ] Lists all 8 endpoints with links to their files
- [ ] References `shared/error-codes.md` for error handling questions

---

## shared/error-codes.md

- [ ] Shows the RFC 9457 `application/problem+json` error format with a real example
- [ ] Status code table includes: 400, 401, 404, 409, 429 (the codes this API actually returns)
- [ ] Retryable column is correct: 429 = Yes, 400/401/404/409 = No
- [ ] Retry strategy mentions `Retry-After` header and `retry_after_seconds` field
- [ ] Does NOT contain endpoint-specific business errors

---

## Endpoint files (spot-check POST /orders and PATCH /customers/{customer_id})

### POST /orders
- [ ] Idempotency section present — required, header = `Idempotency-Key`, window = 24 hours
- [ ] Required fields listed: `customer_id`, `items` (array with `sku`, `quantity`, `unit_amount`)
- [ ] Rate limit mentioned: 120 writes/min
- [ ] Good curl example uses `api.acme.example` (not `example.com`)
- [ ] Common mistakes example shows missing `Idempotency-Key`
- [ ] Error handling says "see `shared/error-codes.md`" for global errors
- [ ] Endpoint-specific errors listed: 404 (customer not found), 409 (idempotency conflict)
- [ ] What This Skill Validates section present

### PATCH /customers/{customer_id}
- [ ] Idempotency section present — required, header = `Idempotency-Key`, window = 24 hours
- [ ] At least one of `name` or `email` required (minProperties: 1)
- [ ] Rate limit mentioned: 120 writes/min
- [ ] Good curl example present
- [ ] Error handling references `shared/error-codes.md`

---

## GET endpoints (spot-check GET /orders)
- [ ] No idempotency section (GET is read-only)
- [ ] Pagination section present — cursor-based, `next_cursor` field, `limit` param (max 100)
- [ ] Rate limit mentioned: 600 reads/min
- [ ] Filter params documented: `customer_id`, `status`

---

## DELETE endpoints (spot-check DELETE /customers/{customer_id})
- [ ] Warning that deletion is **irreversible** (from `x-policy.safety.irreversible: true`)
- [ ] Rate limit mentioned: 60 writes/min (lower limit)
- [ ] Returns 204 (no content) — no response body to parse

---

## Score

Count checked boxes / total boxes. Target: 100% before distributing the skill.

**Known gaps to document if missed:**
- RFC 9457 error format (not standard — many skills default to a generic JSON error)
- `x-policy` metadata (rate limits, idempotency) embedded in the spec
- `retry_after_seconds` in the response body (in addition to the `Retry-After` header)
- `DELETE /customers` is irreversible; `DELETE /orders` (cancel) is not
