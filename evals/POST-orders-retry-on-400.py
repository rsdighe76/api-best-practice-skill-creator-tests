# Eval: POST /orders — Retrying Non-Retryable Errors
#
# This code retries all failed requests including 400 (bad request) and
# 404 (not found). These errors will never succeed on retry — they require
# the request to be fixed first. Retrying wastes rate limit budget and
# can cause unnecessary 429s.

import requests
import time
import uuid

BASE_URL = "https://api.acme.example/v1"
TOKEN = "your_token_here"

def create_order(customer_id: str, items: list) -> dict:
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Idempotency-Key": str(uuid.uuid4())
    }
    payload = {
        "customer_id": customer_id,
        "items": items
    }

    for attempt in range(4):
        response = requests.post(
            f"{BASE_URL}/orders",
            json=payload,
            headers=headers,
            timeout=30
        )
        if response.status_code == 201:
            return response.json()

        # BUG: retrying ALL non-201 responses including 400 and 404
        print(f"Attempt {attempt + 1} failed with {response.status_code}, retrying...")
        time.sleep(2 ** attempt)

    raise Exception("Order creation failed")


# Expected Findings:
#
# 1. Retrying 400 (bad request) — will always fail, wastes rate limit budget
#    Fix: Only retry 429, 500, 502, 503. For 400, raise immediately and
#    fix the request payload.
#
# 2. Retrying 404 (customer not found) — retrying won't create the customer
#    Fix: Catch 404 separately and raise a descriptive error
#
# 3. No Retry-After header check on 429 responses
#    Fix: Read response.headers.get("Retry-After") before sleeping on 429
#
# 4. Max retries is 4 — recommended max is 3
#    Fix: Reduce to max_retries=3


# Pass Criteria:
# [ ] Skill flags retrying 400 errors
# [ ] Skill flags retrying 404 errors
# [ ] Skill flags missing Retry-After header check on 429
