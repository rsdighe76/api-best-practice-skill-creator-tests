---
name: acme-orders-best-practices
description: "Best practices for integrating with the ACME Orders API. Use when: implementing ACME Orders API integration, handling ACME errors, creating customers or orders, troubleshooting ACME API issues."
---

# ACME Orders API — Integration Best Practices

## How to Use This Skill

**This skill validates your ACME Orders API integration against documented best practices.**

**To use, provide one of the following:**
1. Copy/paste your API request (curl, JSON, HTTP format)
2. Upload a file with your integration code
3. Copy/paste your code snippet

**Authoritative Source:**
- This skill uses ONLY the best practices defined in this skill
- All validation rules come from the official ACME API specification
- No web searches or external docs — ensuring accuracy

**What happens next:**
1. I'll identify which endpoint(s) you're calling
2. Load the best practices for that endpoint
3. Validate your implementation
4. Report any issues with specific recommendations

---

## Analysis Process

**When you provide your code, I will:**

1. **Identify which endpoint(s)** you're calling
2. **Determine input type:**
   - Single API request (curl/JSON) → Validate request structure only
   - Full code implementation → Validate everything (request + error handling + retries + timeouts)
3. **Load endpoint-specific best practices** from the URL in the table below
   - For error handling questions, also load `https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices/shared/error-codes.md`
4. **Run validation checks** based on input type:
   - **Request-level:** Authentication, required fields, idempotency headers
   - **Code-level:** Error handling, retry logic, rate limiting, timeouts (for full code only)
5. **Report findings** using this format:
   ```
   ⚠️  Issue: [What's wrong]
   Why: [Consequence]
   Recommendation: [How to fix — code snippet]
   ```
6. **Summary:** Count of issues by category

**Philosophy:**
- These are recommendations, not requirements
- You may have valid reasons to deviate
- If you acknowledge a finding and choose to proceed, that's acceptable

---

## Authentication

All endpoints use **OAuth2 Client Credentials**. Set these environment variables:

```bash
ACME_CLIENT_ID=your_client_id
ACME_CLIENT_SECRET=your_client_secret
ACME_API_BASE_URL=https://api.acme.example/v1
```

Obtain a token before calling any endpoint:

```bash
curl -X POST "https://auth.acme.example/oauth2/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=$ACME_CLIENT_ID" \
  -d "client_secret=$ACME_CLIENT_SECRET" \
  -d "scope=customers:read customers:write orders:read orders:write"
```

Then use the token as a Bearer header on every request:
```bash
-H "Authorization: Bearer <access_token>"
```

There is no dedicated health endpoint — use `GET /customers?limit=1` as a lightweight credential check.

---

## Endpoints

| Method | Path | File |
|--------|------|------|
| POST | /customers | https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices/endpoints/POST-customers.md |
| GET | /customers | https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices/endpoints/GET-customers.md |
| GET | /customers/{customer_id} | https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices/endpoints/GET-customers-customer_id.md |
| PATCH | /customers/{customer_id} | https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices/endpoints/PATCH-customers-customer_id.md |
| DELETE | /customers/{customer_id} | https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices/endpoints/DELETE-customers-customer_id.md |
| POST | /orders | https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices/endpoints/POST-orders.md |
| GET | /orders | https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices/endpoints/GET-orders.md |
| GET | /orders/{order_id} | https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices/endpoints/GET-orders-order_id.md |
| PATCH | /orders/{order_id} | https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices/endpoints/PATCH-orders-order_id.md |
| DELETE | /orders/{order_id} | https://raw.githubusercontent.com/rsdighe76/api-best-practice-skill-creator-tests/master/test-output/acme-orders-best-practices/endpoints/DELETE-orders-order_id.md |

When you provide your code, I'll automatically load the relevant endpoint file(s).
