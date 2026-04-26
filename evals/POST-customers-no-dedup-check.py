# Eval: POST /customers — No Duplicate Check Before Retry
#
# This code retries POST /customers on failure without first checking
# whether the customer was already created. Because POST /customers is
# NOT idempotent, each retry can create a duplicate customer record.

import requests
import time

BASE_URL = "https://api.acme.example/v1"
TOKEN = "your_token_here"

def create_customer(name: str, email: str) -> dict:
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"name": name, "email": email}

    for attempt in range(3):
        response = requests.post(f"{BASE_URL}/customers", json=payload, headers=headers)
        if response.status_code == 201:
            return response.json()
        # Retry on any failure — including network errors
        time.sleep(2 ** attempt)

    raise Exception("Failed to create customer after 3 attempts")


# Expected Findings:
#
# 1. POST /customers is NOT idempotent — retrying may create duplicate customers
#    Fix: Before retrying, call GET /customers?email=<email> to check if the
#    customer already exists. Only proceed with creation if no match is found.
#
# 2. No timeout set on the requests.post() call
#    Fix: Add timeout=30 to requests.post()
#
# 3. Retrying on all failures including potential 400 errors
#    Fix: Only retry on 429, 500, 502, 503 — not on 400/401/404


# Pass Criteria:
# [ ] Skill flags no duplicate check before retry
# [ ] Skill flags missing timeout
# [ ] Skill flags retrying non-retryable errors
