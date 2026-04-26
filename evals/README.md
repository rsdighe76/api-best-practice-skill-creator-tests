# Eval Samples — ACME Orders API Skill

Each file in this directory contains a **deliberately broken** request or code snippet. Run each one through the generated `acme-orders-best-practices` skill and verify it catches the listed issues.

## How to run an eval

1. Open a new Claude conversation with the `acme-orders-best-practices` skill active
2. Paste the contents of an eval file and say: _"Check this against best practices"_
3. Compare the skill's findings against the **Expected Findings** block in the file
4. Mark pass ✅ or fail ❌ for each expected finding

## Eval files

| File | What's broken |
|------|--------------|
| `POST-orders-missing-idempotency-key.md` | No `Idempotency-Key` header |
| `POST-orders-missing-required-fields.md` | Missing `customer_id` and empty `items` |
| `POST-orders-missing-vat-number.md` | EU customer, no `vat_number` |
| `PATCH-orders-missing-idempotency-key.md` | Status update with no idempotency key |
| `POST-customers-no-dedup-check.py` | Retries POST /customers without duplicate check |
| `POST-orders-retry-on-400.py` | Retries all errors including non-retryable 400s |
| `GET-orders-no-pagination.py` | Stops after first page, misses remaining orders |
| `DELETE-customers-no-confirmation.py` | Bulk-deletes customers with no guard |

## Pass criteria

The skill must identify **all** expected findings for a file to pass. Finding extra issues is acceptable. Missing a listed finding is a fail.
