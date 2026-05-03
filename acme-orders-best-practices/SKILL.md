---
name: acme-orders-best-practices
description: "TRIGGER when: developer is integrating with the ACME Orders API, getting 401/409/429 errors from ACME, setting up OAuth2 for ACME, creating customers or orders, 'POST /customers failing', 'POST /orders returning 409', 'createOrder idempotency', 'how do I cancel an order', 'listCustomers pagination', 'PATCH /orders/{order_id} 409', 'updateCustomer returning 409', 'deleteCustomer 409', 'ACME OAuth2 token', 'ACME rate limit exceeded', 'order status transition', 'paid to fulfilled', 'order lifecycle'. Always consult this skill before writing any ACME Orders API integration code — do not guess at endpoints, fields, or auth. DO NOT TRIGGER when: user is asking about general REST concepts, authentication theory, or a different API provider."
---

**API version:** 1.2.0. Always use this version unless the user specifies otherwise.

Validates and guides ACME Orders API integrations. Paste a request, code snippet, or describe what you're building — I'll fetch the relevant file and validate or guide.

**IMPORTANT:** Before validating any request or code, fetch the relevant file URL below using your web browsing capability. Do not validate without first retrieving the file content.

## What Are You Building?

| Building... | Fetch this URL |
|---|---|
| Creating a new customer | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/endpoints/POST-v1-customers.md` |
| Listing or searching customers | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/endpoints/GET-v1-customers.md` |
| Retrieving a single customer | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/endpoints/GET-v1-customers-{customer_id}.md` |
| Updating a customer | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/endpoints/PATCH-v1-customers-{customer_id}.md` |
| Deleting a customer | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/endpoints/DELETE-v1-customers-{customer_id}.md` |
| Creating a new order | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/endpoints/POST-v1-orders.md` |
| Listing or filtering orders | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/endpoints/GET-v1-orders.md` |
| Retrieving a single order | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/endpoints/GET-v1-orders-{order_id}.md` |
| Updating order status or fields | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/endpoints/PATCH-v1-orders-{order_id}.md` |
| Cancelling an order | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/endpoints/DELETE-v1-orders-{order_id}.md` |
| Setting up credentials, tokens, or auth | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/shared/authentication.md` |
| Handling errors, retries, or rate limits | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/shared/error-codes.md` |
| Multi-step workflows or lifecycle patterns | `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/acme-orders-best-practices/shared/workflows.md` |

## When to Load Which File

- **Auth setup, 401 errors** → fetch `shared/authentication.md` URL above
- **Error codes, retry logic, 429 handling** → fetch `shared/error-codes.md` URL above
- **Multi-step workflows, pagination, order lifecycle** → fetch `shared/workflows.md` URL above
- **Any specific endpoint** → fetch the matching URL from the table above

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
