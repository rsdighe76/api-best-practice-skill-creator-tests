# ACME Orders API — Error Reference

Read this file when: you need to understand the error response format, which status codes are retryable, or how to implement retry/backoff logic.

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

`errors[]` is only present on 400 validation failures. `retry_after_seconds` is present on 429 responses alongside the `Retry-After` header.

## Status Codes

| Code | Meaning | Retryable | Action |
|------|---------|:---------:|--------|
| 400 | Validation failed | No | Read `errors[]` and fix the request |
| 401 | Authentication failed | No | Check OAuth2 token and scopes |
| 404 | Resource not found | No | Verify ID exists and includes `cus_` or `ord_` prefix |
| 409 | Conflict — idempotency key reused with different payload | No | Generate a new key |
| 429 | Rate limited | Yes | Wait for `Retry-After` header value |
| 500 | Server error | Yes | Retry with backoff |
| 502 | Bad gateway | Yes | Retry with backoff |
| 503 | Service unavailable | Yes | Retry with backoff |

## Retry Strategies by Endpoint Type

**Retryable for all:** 429, 500, 502, 503. **Non-retryable:** 400, 401, 404, 409.

### GET endpoints
- Initial delay: 500ms · Multiplier: ×2 · Max delay: 8s · Max retries: 3 · No jitter

### POST and PATCH endpoints
- Initial delay: 1s · Multiplier: ×2 + jitter (0–500ms) · Max delay: 30s · Max retries: 3
- Always respect `Retry-After` on 429 — override your timer with the header value

### DELETE endpoints
- Initial delay: 2s · Max retries: 1 (conservative for destructive ops) · No jitter

## Rate Limit Headers

| Header | Meaning |
|--------|---------|
| `X-RateLimit-Limit` | Total requests allowed in the current window |
| `X-RateLimit-Remaining` | Requests left before hitting the limit |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |

**Buckets:** reads 600/min · writes 120/min · deletes 60/min

## Common Mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Retrying a 400 | Same error, wasted quota | Read `errors[]` and fix the request |
| Retrying a 409 | Same conflict | Generate a new idempotency key |
| Ignoring `Retry-After` on 429 | Re-hitting the limit immediately | Use the header value as your wait time |
| Using the same backoff for all endpoint types | Over-waiting on reads | Apply type-specific strategies above |
| Retrying DELETEs aggressively | Risk of unintended double-deletion | Max 1 retry, 2s delay |
