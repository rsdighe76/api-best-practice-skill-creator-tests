# ACME Orders API — Error Reference

## Error Response Format

All errors from the ACME Orders API follow RFC 9457 Problem Details:

```json
{
  "type": "https://api.acme.example/problems/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The field 'email' must be a valid email address.",
  "instance": "/v1/customers",
  "request_id": "req_01HX9P2C7YQ2GQ7P9R8F2H2Z7A",
  "retry_after_seconds": null,
  "errors": [
    {
      "field": "email",
      "code": "invalid_format",
      "message": "Must be a valid email address."
    }
  ]
}
```

On 429 responses, `retry_after_seconds` will be a non-null integer. Always prefer it over a fixed wait.

## Status Codes

| Code | Meaning | Retryable | Action |
|------|---------|:---------:|--------|
| 400  | Bad request — invalid or missing parameters | No | Fix the request; read `errors` array for field-level detail |
| 401  | Authentication failed — token missing or expired | No | Re-fetch an OAuth2 token and retry |
| 403  | Forbidden — token is missing a required scope | No | Re-request the token with the correct scope |
| 404  | Resource not found | No | Check the ID; do not retry with the same ID |
| 409  | Conflict — duplicate idempotency key with different payload, or invalid state transition | No | Read `detail` field; do not retry blindly |
| 429  | Rate limited | Yes | Wait `retry_after_seconds` from the response body before retrying |
| 500  | Server error | Yes | Retry with exponential backoff |
| 502  | Bad gateway | Yes | Retry with exponential backoff |
| 503  | Service unavailable | Yes | Retry with exponential backoff |

## Retry Strategy

**Retryable errors:** 429, 500, 502, 503

**Non-retryable errors:** 400, 401, 403, 404, 409

**Backoff approach:**
- Initial delay: 1 second
- Multiplier: exponential — `delay = 1 * (2 ** attempt)`
- Jitter: add random 0–500ms to avoid thundering herd
- Max delay: 30 seconds
- Max retries: 3
- On 429: always use `retry_after_seconds` from the response body if present; fall back to calculated backoff if absent

```python
import time, random

def retry_with_backoff(fn, max_retries=3):
    retryable = {429, 500, 502, 503}
    for attempt in range(max_retries + 1):
        response = fn()
        if response.status_code not in retryable or attempt == max_retries:
            return response
        if response.status_code == 429:
            wait = response.json().get("retry_after_seconds") or (2 ** attempt)
        else:
            wait = min(2 ** attempt + random.uniform(0, 0.5), 30)
        time.sleep(wait)
```

## Common Mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Retrying a 400 | Wasted requests, same error every time | Fix the request payload first |
| Retrying a 409 | Potential duplicate or continued bad state | Read `detail` to understand the conflict |
| Ignoring `retry_after_seconds` on 429 | Retrying too fast, staying rate-limited | Always read the field from the response body |
| Catching all errors the same way | Missing recoverable vs permanent failures | Branch on `status` code first, then handle |
