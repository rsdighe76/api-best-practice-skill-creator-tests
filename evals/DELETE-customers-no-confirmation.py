# Eval: DELETE /customers — Bulk Delete Without Confirmation Guard
#
# This code loops over a list of customer IDs and deletes them all without
# any confirmation step. DELETE /customers is IRREVERSIBLE — there is no
# undo. A bug in the caller or a wrong list of IDs will permanently destroy
# customer records.

import requests

BASE_URL = "https://api.acme.example/v1"
TOKEN = "your_token_here"

def bulk_delete_customers(customer_ids: list) -> None:
    headers = {"Authorization": f"Bearer {TOKEN}"}

    # BUG: no confirmation step, no dry-run, no logging before deletion
    for customer_id in customer_ids:
        response = requests.delete(
            f"{BASE_URL}/customers/{customer_id}",
            headers=headers
        )
        if response.status_code == 204:
            print(f"Deleted {customer_id}")
        else:
            print(f"Failed to delete {customer_id}: {response.status_code}")


# Expected Findings:
#
# 1. No confirmation step before irreversible bulk deletion
#    Fix: Add an explicit confirmation prompt or dry-run mode before deleting:
#
#    print(f"About to permanently delete {len(customer_ids)} customers. Type YES to confirm:")
#    if input().strip() != "YES":
#        print("Aborted.")
#        return
#
# 2. No timeout set on requests.delete()
#    Fix: Add timeout=30
#
# 3. Errors are printed and silently skipped — deletion continues even after failure
#    Fix: Raise on unexpected errors or collect failures and report after the loop
#
# 4. No rate limit handling — at high volume, will hit the 60/min delete limit
#    Fix: Track X-RateLimit-Remaining and back off when low


# Pass Criteria:
# [ ] Skill flags irreversible bulk deletion with no confirmation guard
# [ ] Skill flags missing timeout
# [ ] Skill flags silent error handling
# [ ] Skill flags no rate limit handling for delete bucket (60/min)
