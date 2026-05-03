# Eval: Delete Customer Workflow — Missing Order Cancellation
#
# This code tries to delete a customer directly without first cancelling
# their open orders. The API returns 409 if the customer has active orders.
# Even if it "works" for customers with no orders, it will fail silently
# for customers that have them — and the error is not handled.

import requests

BASE_URL = "https://api.acme.example/v1"
TOKEN = "your_token_here"

def delete_customer(customer_id: str) -> None:
    headers = {"Authorization": f"Bearer {TOKEN}"}

    # BUG: jumps straight to delete without cancelling open orders first
    response = requests.delete(
        f"{BASE_URL}/customers/{customer_id}",
        headers=headers,
        timeout=30
    )

    # BUG: treats 409 as a generic failure with no recovery guidance
    if response.status_code != 204:
        print(f"Delete failed: {response.status_code}")


# Expected Findings:
#
# 1. No prerequisite order cancellation before DELETE /customers
#    Fix: Before deleting, paginate GET /orders?customer_id=<id>&status=created
#    and GET /orders?customer_id=<id>&status=paid — cancel all open orders,
#    then delete the customer
#
# 2. 409 response not handled with recovery guidance
#    Fix: A 409 on DELETE /customers means open orders exist — catch it
#    explicitly, cancel those orders, then retry the delete
#
# 3. 204 success not distinguished from other non-error codes
#    Fix: Assert status_code == 204 explicitly; do not parse a response body


# Pass Criteria:
# [ ] Skill flags missing order cancellation before customer deletion
# [ ] Skill flags 409 not handled with recovery (cancel orders then retry)
# [ ] Skill flags 204 not explicitly checked
