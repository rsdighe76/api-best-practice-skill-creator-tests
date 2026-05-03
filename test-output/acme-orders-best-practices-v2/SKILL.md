---
name: acme-orders-best-practices
description: "TRIGGER when: developer is calling POST /customers, POST /orders, PATCH /orders, getting 409 idempotency conflicts on order creation, hitting 429 rate limits, building customer onboarding, placing orders, paginating order history, advancing order to paid or fulfilled, cancelling orders, getting 404 on cus_ or ord_ IDs, asking about ACME auth or OAuth2 scopes. Always consult this skill before writing any ACME Orders API integration code — do not guess at endpoints, fields, or auth. DO NOT TRIGGER when: user is asking about general REST concepts, authentication theory, or a different API provider."
---

**API version:** 1.2.0. Always use this version unless the user specifies otherwise.

Validates and guides ACME Orders API integrations. Paste a request, code snippet, or describe what you're building — I'll load the relevant file and validate or guide.

## What Are You Building?

| Building... | Load this file |
|---|---|
| Creating a customer | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/endpoints/POST-customers.md` |
| Listing or searching customers | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/endpoints/GET-customers.md` |
| Retrieving a customer by ID | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/endpoints/GET-customers-customer_id.md` |
| Updating a customer | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/endpoints/PATCH-customers-customer_id.md` |
| Deleting a customer | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/endpoints/DELETE-customers-customer_id.md` |
| Placing an order | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/endpoints/POST-orders.md` |
| Listing or filtering orders | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/endpoints/GET-orders.md` |
| Retrieving an order by ID | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/endpoints/GET-orders-order_id.md` |
| Advancing order status (paid, fulfilled) | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/endpoints/PATCH-orders-order_id.md` |
| Cancelling an order | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/endpoints/DELETE-orders-order_id.md` |
| Setting up credentials, tokens, or auth | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/shared/authentication.md` |
| Handling errors, retries, or rate limits | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/shared/error-codes.md` |
| Multi-step workflows or lifecycle patterns | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/shared/workflows.md` |

## When to Load Which File

- **Auth setup, credentials, token acquisition** → load `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/shared/authentication.md`
- **Error codes, retry logic, rate limits** → load `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/shared/error-codes.md`
- **Multi-step workflows, lifecycle patterns** → load `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices-v2/shared/workflows.md`
- **Any customer operation** → load the matching `endpoints/` URL from the table above
- **Any order operation** → load the matching `endpoints/` URL from the table above

Validate a **single request (curl/JSON)** → check request structure only.
Validate **full code** → check request + error handling + retries + timeouts.

## Validation Format

All findings use this format:

```
⚠️ Issue: [what is wrong]
Why: [consequence if ignored]
Recommendation: [how to fix — before/after code]
Note: If you have a valid reason to deviate, acknowledge and proceed.
```
