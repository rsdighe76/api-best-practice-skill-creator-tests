# Eval: Order Lifecycle — Wrong Transition Order + No State Check
#
# This code tries to mark an order as "fulfilled" directly from "created",
# skipping the required "paid" intermediate state. It also doesn't check
# the current order status before attempting the transition, and doesn't
# store the idempotency key before calling the API.

import requests
import uuid

BASE_URL = "https://api.acme.example/v1"
TOKEN = "your_token_here"

def fulfill_order(order_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    # BUG: no GET to check current status before attempting transition
    # If order is already fulfilled or cancelled, this call will fail or
    # produce unexpected behaviour

    # BUG: jumps straight to "fulfilled" — skips required "paid" state
    # The API enforces: created → paid → fulfilled
    response = requests.patch(
        f"{BASE_URL}/orders/{order_id}",
        json={"status": "fulfilled"},
        headers={
            **headers,
            # BUG: key generated here, not stored before the call
            "Idempotency-Key": str(uuid.uuid4())
        },
        timeout=30
    )
    response.raise_for_status()
    return response.json()


# Expected Findings:
#
# 1. No GET /orders/{id} before PATCH to confirm current status
#    Fix: Always fetch and check current status before attempting a transition;
#    if already at target state, treat as success and skip the PATCH
#
# 2. Skips required "paid" intermediate state — tries created → fulfilled directly
#    Fix: Follow the valid transition sequence:
#    created → paid (PATCH status=paid) → fulfilled (PATCH status=fulfilled)
#    The server enforces this order and will reject the skip
#
# 3. Idempotency key generated inside the call expression — not stored before
#    Fix: Generate and persist the key before the requests.patch() call
#    so it can be reused if the call needs to be retried


# Pass Criteria:
# [ ] Skill flags missing status check before PATCH (no GET first)
# [ ] Skill flags invalid lifecycle transition (created → fulfilled skips paid)
# [ ] Skill flags idempotency key not stored before the API call
