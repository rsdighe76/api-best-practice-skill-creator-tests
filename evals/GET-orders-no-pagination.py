# Eval: GET /orders — No Pagination Loop
#
# This code fetches a single page of orders and stops, assuming it has
# received all orders. For customers with more than 20 orders (the default
# page size), this silently misses records.

import requests

BASE_URL = "https://api.acme.example/v1"
TOKEN = "your_token_here"

def get_customer_orders(customer_id: str) -> list:
    headers = {"Authorization": f"Bearer {TOKEN}"}

    # BUG: fetches only the first page — stops even if next_cursor is present
    response = requests.get(
        f"{BASE_URL}/orders",
        params={"customer_id": customer_id, "limit": 20},
        headers=headers,
        timeout=10
    )
    response.raise_for_status()
    return response.json()["data"]


# Expected Findings:
#
# 1. No pagination loop — stops after first page
#    Fix: Loop until next_cursor is null:
#
#    cursor = None
#    all_orders = []
#    while True:
#        params = {"customer_id": customer_id, "limit": 100}
#        if cursor:
#            params["cursor"] = cursor
#        response = requests.get(f"{BASE_URL}/orders", params=params, headers=headers, timeout=10)
#        data = response.json()
#        all_orders.extend(data["data"])
#        cursor = data.get("next_cursor")
#        if not cursor:
#            break
#    return all_orders
#
# 2. Using limit=20 (default) instead of limit=100 (max)
#    Fix: Use limit=100 to minimise number of API calls


# Pass Criteria:
# [ ] Skill flags no pagination loop (next_cursor never checked)
# [ ] Skill flags suboptimal page size (optional — using 20 instead of max 100)
