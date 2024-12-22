import requests
import json
from datetime import datetime
from bankfrick_connect import get_jwt_token


BASE_URL = "https://olb.bankfrick.li/webapi/v2" # Configuration settings for connecting to the Bank Frick API
TRANSACTIONS_ENDPOINT = "/transactions"
IPLICIT_API_URL = "https://api.iplicit.com/transactions"
IPLICIT_API_KEY = "Placeholder"

# Account mapping: Links account IDs to their human-readable names and currencies
account_mapping = {

}

def fetch_transactions(jwt_token, account_id, start_date, end_date):
    """
    Fetch transactions for a specific account and date range.
    """
    url = f"{BASE_URL}{TRANSACTIONS_ENDPOINT}?accountId={account_id}&fromDate={start_date}&toDate={end_date}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
    }

    print(f"Fetching transactions for account {account_id}...")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Transactions fetched successfully.")
        response_json = response.json()
        return response_json.get("transactions", []) if isinstance(response_json, dict) else response_json
    else:
        print(f"Failed to fetch transactions for {account_id}: {response.status_code} - {response.text}")
        return []

def post_transaction_to_iplicit(api_key, payload):
    """
    Post a single transaction to the Iplicit API.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print(f"Posting payload: {json.dumps(payload, indent=4)}")
    response = requests.post(IPLICIT_API_URL, headers=headers, json=payload)

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    if response.status_code in (200, 201):
        print(f"Successfully posted transaction: {payload.get('Description', 'N/A')}")
    else:
        print(f"Error posting transaction: {response.text}")

def process_and_post_transactions(jwt_token):
    """
    Fetch, process, and post transactions to Iplicit for the current month.
    """
    start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d') # Start of Month
    end_date = datetime.now().strftime('%Y-%m-%d')

    for account_id, account_info in account_mapping.items():   # Iterate through each account and process thier  transactions
        transactions = fetch_transactions(jwt_token, account_id, start_date, end_date)

        if not transactions:
            print(f"No transactions found for {account_info['name']}.")
            continue

        for transaction in transactions:
            payload = { # Build payload for Iplicit API
                "LegalEntity": "",
                "BankAccount": account_info["bank_account"],
                "Code": account_info["code"],
                "TransactionDate": transaction.get("valuta"),
                "Amount": -abs(transaction.get("amount", 0)) if transaction.get("direction") == "outgoing" else abs(transaction.get("amount", 0)),
                "Reference": transaction.get("type", "N/A"),
                "Description": transaction.get("creditor", {}).get("name", "N/A")
            }
            post_transaction_to_iplicit(IPLICIT_API_KEY, payload)

def main():
    """
    Main function to fetch transactions and post to Iplicit.
    """
    jwt_token = get_jwt_token() # Retrieve JWT token for Bank Frick API from bankfrick_connect
    if not jwt_token:
        print("Failed to retrieve JWT token. Exiting.")
        return

    process_and_post_transactions(jwt_token)

if __name__ == "__main__":
    main()
