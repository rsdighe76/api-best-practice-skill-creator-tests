---
name: acme-orders-best-practices
description: "TRIGGER when: developer is integrating with the ACME Orders API, getting 401/409/429 errors from ACME, setting up OAuth2 for ACME, creating customers or orders, 'POST /customers failing', 'POST /orders returning 409', 'createOrder idempotency', 'how do I cancel an order', 'listCustomers pagination', 'PATCH /orders/{order_id} 409', 'updateCustomer returning 409', 'deleteCustomer 409', 'ACME OAuth2 token', 'ACME rate limit exceeded', 'order status transition', 'paid to fulfilled', 'order lifecycle'. Always consult this skill before writing any ACME Orders API integration code — do not guess at endpoints, fields, or auth. DO NOT TRIGGER when: user is asking about general REST concepts, authentication theory, or a different API provider."
---

**API version:** 1.2.0. Always use this version unless the user specifies otherwise.

Validates and guides ACME Orders API integrations. Paste a request, code snippet, or describe what you're building — I'll read the relevant file and validate or guide.

**IMPORTANT:** Before validating any request or code, read the relevant file from the table below. Do not validate without first reading the file content.

## What Are You Building?

| Building... | Read this file |
|---|---|
| Creating a new customer | `endpoints/POST-v1-customers.md` |
| Listing or searching customers | `endpoints/GET-v1-customers.md` |
| Retrieving a single customer | `endpoints/GET-v1-customers-{customer_id}.md` |
| Updating a customer | `endpoints/PATCH-v1-customers-{customer_id}.md` |
| Deleting a customer | `endpoints/DELETE-v1-customers-{customer_id}.md` |
| Creating a new order | `endpoints/POST-v1-orders.md` |
| Listing or filtering orders | `endpoints/GET-v1-orders.md` |
| Retrieving a single order | `endpoints/GET-v1-orders-{order_id}.md` |
| Updating order status or fields | `endpoints/PATCH-v1-orders-{order_id}.md` |
| Cancelling an order | `endpoints/DELETE-v1-orders-{order_id}.md` |
| Setting up credentials, tokens, or auth | `shared/authentication.md` |
| Handling errors, retries, or rate limits | `shared/error-codes.md` |
| Multi-step workflows or lifecycle patterns | `shared/workflows.md` |

## When to Load Which File

- **Auth setup, 401 errors** → read `shared/authentication.md`
- **Error codes, retry logic, 429 handling** → read `shared/error-codes.md`
- **Multi-step workflows, pagination, order lifecycle** → read `shared/workflows.md`
- **Any specific endpoint** → read the matching file from the table above

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
