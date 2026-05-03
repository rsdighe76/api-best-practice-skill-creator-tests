# ACME Orders API — Authentication

Read this file when: you are setting up credentials for the first time, getting 401 errors, or need to know which OAuth2 scopes to request.

## Credentials Setup

Set these environment variables before running any code:

```bash
export ACME_CLIENT_ID=your_client_id
export ACME_CLIENT_SECRET=your_client_secret
export ACME_API_BASE_URL=https://api.acme.example/v1
```

## Getting a Token

ACME Orders API uses OAuth2 Client Credentials:

```bash
curl -X POST "https://auth.acme.example/oauth2/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=$ACME_CLIENT_ID" \
  -d "client_secret=$ACME_CLIENT_SECRET" \
  -d "scope=customers:read customers:write orders:read orders:write"
```

Extract `access_token` from the response and pass it as a Bearer header on every request:

```bash
-H "Authorization: Bearer $ACME_TOKEN"
```

Tokens expire — handle 401 responses by re-fetching a token and retrying the original request once.

## Scopes

| Scope | What it grants |
|-------|---------------|
| `customers:read` | GET /customers, GET /customers/{id} |
| `customers:write` | POST /customers, PATCH /customers/{id}, DELETE /customers/{id} |
| `orders:read` | GET /orders, GET /orders/{id} |
| `orders:write` | POST /orders, PATCH /orders/{id}, DELETE /orders/{id} |

Request only the scopes your integration needs.

## Verifying Credentials

No dedicated health endpoint. Use this as a lightweight credential check:

```bash
curl -G "https://api.acme.example/v1/customers" \
  -H "Authorization: Bearer $ACME_TOKEN" \
  --data-urlencode "limit=1"
```

A `200` confirms your token and `customers:read` scope are valid.

## Common Auth Errors

- **401** — token missing, expired, or malformed; re-fetch a token and retry once
- **403** — token valid but missing required scope; re-request with the correct scopes
