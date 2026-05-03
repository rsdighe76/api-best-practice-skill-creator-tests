# ACME Orders API — Authentication

Read this file when: you are setting up credentials for the first time, getting 401 errors, or need to know which scopes to request.

## Credentials Setup

Set these environment variables before running any code:

```bash
export ACME_CLIENT_ID=your_client_id
export ACME_CLIENT_SECRET=your_client_secret
export ACME_BASE_URL=https://api.acme.example/v1
export ACME_TOKEN_URL=https://auth.acme.example/oauth2/token
```

## Getting a Token

ACME Orders API uses OAuth2 Client Credentials:

```bash
curl -X POST "$ACME_TOKEN_URL" \
  -d "grant_type=client_credentials" \
  -d "client_id=$ACME_CLIENT_ID" \
  -d "client_secret=$ACME_CLIENT_SECRET" \
  -d "scope=customers:read customers:write orders:read orders:write"
```

Extract `access_token` from the response and pass it as a Bearer header on every request:

```bash
-H "Authorization: Bearer $ACME_ACCESS_TOKEN"
```

Tokens expire — check `expires_in` in the response and refresh before expiry rather than waiting for a 401.

## Scopes

| Scope | What it grants |
|-------|---------------|
| `customers:read` | Read customer records — GET /customers, GET /customers/{id} |
| `customers:write` | Create, update, and delete customers |
| `orders:read` | Read order records — GET /orders, GET /orders/{id} |
| `orders:write` | Create, update, and cancel orders |

Request only the scopes your integration needs. A read-only reporting integration should request `customers:read orders:read` only.

## Verifying Credentials

After setup, call this to confirm your token and scopes are working:

```bash
curl "$ACME_BASE_URL/customers?limit=1" \
  -H "Authorization: Bearer $ACME_ACCESS_TOKEN"
```

A 200 response confirms auth is working. A 401 means the token is missing or malformed. A 403 means the token is valid but is missing the `customers:read` scope.

## Common Auth Errors

- **401** — token missing, expired, or malformed; re-fetch a token using the client credentials flow above and retry
- **403** — token is valid but missing a required scope; re-request the token including the correct scope
