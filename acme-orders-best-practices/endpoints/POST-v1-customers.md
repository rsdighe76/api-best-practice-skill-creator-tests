# POST /v1/customers

Read this file when: you are creating a new ACME customer and want to know what's required, what context-dependent fields apply, or how to handle a failed create safely.

## The Working Request

```bash
curl -X POST "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane.doe@acme-customer.com"
  }'
```

## Gotchas

- **No idempotency support.** If your POST fails with a network error, do NOT retry blindly — the customer may already have been created. Always `GET /customers?email=<email>` first to check. See `shared/workflows.md` workflow 1.
- **Email must be globally unique.** Sending the same email twice returns 400 with `code: duplicate_email`. Check for existence before creating, or handle the 400 explicitly.
- **Enterprise customers require `company_name`.** If you are onboarding an Enterprise segment customer, you must include `company_name` or the request is rejected with 400.
- **EU customers require `vat_number`.** If `billing_country` is any EU member state (AT, BE, BG, HR, CY, CZ, DK, EE, FI, FR, DE, GR, HU, IE, IT, LV, LT, LU, MT, NL, PL, PT, RO, SK, SI, ES, SE), you must include `vat_number`.

## What Fails ❌

```bash
# Missing required field
curl -X POST "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe"}'
# → 400: email is required

# EU customer without vat_number
curl -X POST "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Hans Müller", "email": "hans@example.de", "billing_country": "DE"}'
# → 400: vat_number is required for EU billing countries
```

## Required Fields

**Always required:**
- `name` (string, minLength: 1) — customer's full name
- `email` (string, email format) — must be unique across all customers

**Context-dependent:**
- `company_name` (string) — required when onboarding an Enterprise segment customer
- `vat_number` (string) — required when `billing_country` is an EU member state
- `billing_country` (string, ISO 3166-1 alpha-2) — required when `vat_number` is present

**Do NOT send:**
- `id` — assigned server-side
- `created_at`, `updated_at` — set server-side

## For Full Code Implementations

**Error handling:**
- For global error codes, retry rules, and error format: see `shared/error-codes.md`
- Endpoint-specific errors:
  - `400 duplicate_email` — customer with this email already exists; use GET /customers?email= to retrieve their ID
  - `400 missing_vat_number` — EU billing_country provided without vat_number
  - `400 missing_company_name` — Enterprise segment customer requires company_name
  - `401` — re-fetch OAuth2 token with `customers:write` scope
  - `429` — rate limited; wait `retry_after_seconds` from response body

**Timeout:** 30 seconds.

**Rate limit:** 120 requests/minute (write bucket). POST /customers is not retryable on error — check for existence first.

## What This Skill Validates

**Request-level checks:**
- ✓ `Authorization: Bearer` header present (requires `customers:write` scope)
- ✓ `Content-Type: application/json` header present
- ✓ `name` field included and non-empty
- ✓ `email` field included and valid email format
- ✓ `company_name` included when customer segment is Enterprise
- ✓ `vat_number` included when `billing_country` is an EU member state

**Code-level checks (full implementations only):**
- ✓ Timeout set to 30 seconds
- ✓ 400 handled separately from 5xx — not retried
- ✓ `errors` array inspected for field-level detail on 400
- ✓ 429 handled with `retry_after_seconds` wait
- ✓ After network error, `GET /customers?email=` called before retrying the POST
