# Eval: Checkout Workflow — No Duplicate Customer Check
#
# This code goes straight to POST /customers without checking if the customer
# already exists. On any retry (network error, timeout, re-submission), it
# creates a duplicate customer record. POST /customers is NOT idempotent.

import requests
import uuid

BASE_URL = "https://api.acme.example/v1"
TOKEN = "your_token_here"

def checkout(name: str, email: str, items: list) -> dict:
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    # BUG: no check — blindly creates customer on every call
    customer_resp = requests.post(
        f"{BASE_URL}/customers",
        json={"name": name, "email": email},
        headers=headers,
        timeout=30
    )
    customer_resp.raise_for_status()
    customer_id = customer_resp.json()["id"]

    # BUG: idempotency key generated after the customer call — if customer
    # creation fails mid-flight and we retry the whole function, we get a
    # new key and a new duplicate order attempt
    idempotency_key = str(uuid.uuid4())

    order_resp = requests.post(
        f"{BASE_URL}/orders",
        json={"customer_id": customer_id, "items": items},
        headers={**headers, "Idempotency-Key": idempotency_key},
        timeout=30
    )
    order_resp.raise_for_status()
    return order_resp.json()


# Expected Findings:
#
# 1. No duplicate customer check before POST /customers
#    Fix: Call GET /customers?email=<email> first; only POST if not found
#
# 2. Idempotency key for POST /orders generated inside the function body
#    (not stored before the call) — if the function is retried, a new key
#    is generated and the previous order attempt cannot be safely recovered
#    Fix: Generate and persist the idempotency key before calling POST /customers,
#    so the same key can be reused on any retry of the full checkout


# Pass Criteria:
# [ ] Skill flags no dedup check before POST /customers
# [ ] Skill flags idempotency key not stored before the API call
