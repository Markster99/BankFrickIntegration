import requests
import csv
import os
from datetime import datetime, timedelta
from bankfrick_connect import get_jwt_token

# Configuration settings for connecting to the Bank Frick API
BASE_URL = "https://olb.bankfrick.li/webapi/v2"
TRANSACTIONS_ENDPOINT = "/transactions"
OUTPUT_DIR = "/workspaces/15932103/Project/output/" # Output directory for CSV files

# Account mapping: Links account IDs to their human-readable names and currencies
account_mapping = {

}

def fetch_transactions(jwt_token, account_id, date):
    """
    Fetch transactions for a specific account and date.
    """
    url = f"{BASE_URL}{TRANSACTIONS_ENDPOINT}?accountId={account_id}&fromDate={date}&toDate={date}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
    }

    print(f"Fetching transactions for account {account_id} on {date}...")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Transactions fetched successfully for account {account_id}.")
        response_json = response.json()
        if isinstance(response_json, dict) and "transactions" in response_json:
            return response_json.get("transactions", [])
        elif isinstance(response_json, list):
            return response_json
        else:
            print(f"Unexpected response format: {response_json}")
            return []
    else:
        print(f"Failed to fetch transactions for account {account_id}: {response.status_code} - {response.text}")
        return []

def process_transactions(transactions, account_name, currency, date):
    """
    Process transactions and generate summary.
    """
    count = len(transactions)
    formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
    if count > 0:
        print(f"{account_name} had {count} transactions on {formatted_date}.")
        return count
    else:
        print(f"{account_name} had no movements on {formatted_date}.")
        return 0

def main():
    """
    Main script to fetch transactions from yesterday for all accounts and generate a summary.
    """
    # Get the JWT token
    jwt_token = get_jwt_token()
    if not jwt_token:
        print("Failed to retrieve JWT token. Exiting.")
        return

    # Get yesterday's date
    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    accounts_endpoint = f"{BASE_URL}/accounts" # Fetch the list of accounts available from the API
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
    }
    print("Fetching account list...")
    response = requests.get(accounts_endpoint, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch accounts: {response.status_code} - {response.text}")
        return

    # Extract accounts from the API response
    response_json = response.json()
    accounts = response_json.get("accounts", [])

    # Initialize summary list to store results for all accounts
    summary = []

    # Iterate over each account and fetch transactions
    for account in accounts:
        account_id = account.get("account")
        currency = account.get("currency")
        account_name = account_mapping.get(account_id, "Unknown")

        if not account_id or not account_name or not currency:
            continue # Skip accounts with incomplete data

        # Fetch transactions for the account
        transactions = fetch_transactions(jwt_token, account_id, date)

        # Process transactions and generate summary
        transaction_count = process_transactions(transactions, account_name, currency, date)
        summary.append((account_name, currency, transaction_count))

    # Print the daily summary for all accounts
    print("\nDaily Transaction Summary:")
    formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
    for entry in summary:
        account_name, currency, transaction_count = entry
        if transaction_count > 0:
            print(f"{account_name} had {transaction_count} transactions on {formatted_date}.")
        else:
            print(f"{account_name} had no movements on {formatted_date}.")

if __name__ == "__main__":
    main()
