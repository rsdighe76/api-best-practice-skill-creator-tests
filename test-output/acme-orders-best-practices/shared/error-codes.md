# ACME Orders API — Error Reference

## Error Response Format

All errors use RFC 9457 `application/problem+json`:

```json
{
  "type": "https://api.acme.example/problems/validation-error",
  "title": "Validation error",
  "status": 400,
  "detail": "Request validation failed.",
  "instance": "/v1/customers",
  "request_id": "req_01HX9R2EXAMPLE",
  "errors": [
    {
      "field": "email",
      "code": "invalid_format",
      "message": "Must be a valid email address."
    }
  ]
}
```

`errors[]` is only present on 400 validation failures. `retry_after_seconds` is present on 429 responses.

---

## Status Codes

| Code | Meaning | Retryable | Action |
|------|---------|:---------:|--------|
| 400 | Validation failed | No | Fix the request — read `errors[]` for field details |
| 401 | Authentication failed | No | Check OAuth2 token and scopes |
| 404 | Resource not found | No | Verify the ID exists and uses correct prefix (`cus_`, `ord_`) |
| 409 | Conflict — idempotency key reused with different payload | No | Use a new idempotency key |
| 429 | Rate limited | Yes | Wait for `Retry-After` header value (seconds) |
| 500 | Server error | Yes | Retry with exponential backoff |
| 502 | Bad gateway | Yes | Retry with exponential backoff |
| 503 | Service unavailable | Yes | Retry with exponential backoff |

---

## Retry Strategy

**Retryable:** 429, 500, 502, 503

**Non-retryable:** 400, 401, 404, 409 — these will not succeed on retry without fixing the request.

**Backoff approach:**
- Initial delay: 1 second
- Multiplier: exponential — `delay × 2^attempt`
- Jitter: add random 0–500ms to avoid thundering herd
- Max delay: 30 seconds
- Max retries: 3
- Always respect `Retry-After` header on 429 — ignore your own backoff timer and wait the specified seconds

**Example (Python):**
```python
import time, random

def with_retry(fn, max_retries=3):
    delay = 1.0
    for attempt in range(max_retries + 1):
        response = fn()
        if response.status_code not in (429, 500, 502, 503):
            return response
        if attempt == max_retries:
            raise Exception(f"Failed after {max_retries} retries")
        if response.status_code == 429:
            delay = float(response.headers.get("Retry-After", delay))
        else:
            delay = min(delay * (2 ** attempt) + random.uniform(0, 0.5), 30)
        time.sleep(delay)
```

---

## Rate Limit Headers

On every response, check these headers to track usage proactively:

| Header | Meaning |
|--------|---------|
| `X-RateLimit-Limit` | Total requests allowed in the current window |
| `X-RateLimit-Remaining` | Requests remaining before you hit the limit |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |

**Rate limit buckets:**
- Read endpoints (GET): 600 requests/minute
- Write endpoints (POST, PATCH): 120 requests/minute
- Delete endpoints (DELETE): 60 requests/minute

---

## Common Mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Retrying a 400 | Same error, wasted requests | Read `errors[]` and fix the request |
| Retrying a 409 | Same conflict | Generate a new idempotency key |
| Ignoring `Retry-After` on 429 | Getting blocked longer | Use the header value as your wait time |
| Retrying without backoff | Immediate re-rate-limit | Add exponential backoff with jitter |
| Stripping `cus_` or `ord_` prefix from IDs | 404 not found | Always pass the full ID including prefix |
