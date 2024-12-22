import requests
import csv
import json
import os
from datetime import datetime, timedelta
from bankfrick_connect import get_jwt_token  # This pulls in from 1st file so Dependency remains intact

# Configuration settings for connecting to the Bank Frick API
BASE_URL = "https://olb.bankfrick.li/webapi/v2"
TRANSACTIONS_ENDPOINT = "/transactions"
OUTPUT_DIR = "/workspaces/15932103/Project/output/"  # Output directory for CSV files

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

    print(f"Fetching transactions for account {account_id} from {start_date} to {end_date}...")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Transactions fetched successfully for account {account_id}.")
        response_json = response.json()
        if isinstance(response_json, dict) and "transactions" in response_json:
            return response_json
        elif isinstance(response_json, list):
            return {"transactions": response_json}
        else:
            print(f"Unexpected response format: {response_json}")
            return {"transactions": []}
    else:
        print(f"Failed to fetch transactions for account {account_id}: {response.status_code} - {response.text}")
        return {"transactions": []}


def save_transactions_to_csv(filtered_transactions, account_name, currency):
    """
    Save the filtered transactions into a CSV file for the given account and currency.
    """
    if not filtered_transactions:
        print(f"No transactions to save for {account_name} in {currency}.")
        return

    # Make sures OUTPUT_DIR exists so it can actually output, otherwise it'll  spit out can't find error
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Make file name sanitized and create file path so it can output correctly
    sanitized_account_name = account_name.replace("/", "_").replace(" ", "_")
    output_file_name = f"{sanitized_account_name}_{datetime.now().strftime('%Y-%m-%d')}.csv"
    output_file_path = os.path.join(OUTPUT_DIR, output_file_name)

    # Write the transactions to CSV file
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Amount", "Currency", "Debitor Account", "Creditor Name", "Merchant Name"])

        for transaction in filtered_transactions:
            merchant_name = transaction.get("creditor", {}).get("name")
            debitor_account = transaction.get("debitor", {}).get("accountNumber")
            debitor_name = account_mapping.get(debitor_account, "Unknown")

            # Adjust the amount for incoming and outgoing transactions
            direction = transaction.get("direction")
            amount = transaction.get("amount")
            if direction == "outgoing":
                amount = -abs(amount)  # Ensure it's negative for debits
                description = f"Payment to {merchant_name}"
            elif direction == "incoming":
                amount = abs(amount)  # Ensure it's positive for credits
                description = f"Received from {debitor_name}"
            else:
                description = "Unknown transaction"

            # Write the transaction details to the CSV
            writer.writerow([
                transaction.get("valuta"),
                description,
                amount,
                transaction.get("currency"),
                debitor_name,
                transaction.get("creditor", {}).get("name"),
                merchant_name
            ])

    print(f"Saved transactions to {output_file_path}")


def filter_transactions(transactions, account_id):
    """
    Filter transactions to only include those associated with the given account ID.
    """
    return [
        transaction for transaction in transactions
        if transaction.get("debitor", {}).get("accountNumber") == account_id
    ]

def main():
    """
    Main script to fetch and save transactions for all accounts grouped by currency.
    """
    jwt_token = get_jwt_token() # Obtain a JWT token using my earlier Bank Frick connection script
    if not jwt_token:
        print("Failed to retrieve JWT token. Exiting.")
        return

    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  # Yesterday
    start_date = (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d')  # 1 week before yesterday

    accounts_endpoint = f"{BASE_URL}/accounts"  # Fetch the list of accounts available from the API
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
    }
    print("Fetching account list...")
    response = requests.get(accounts_endpoint, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch accounts: {response.status_code} - {response.text}")
        return

    response_json = response.json()
    accounts = response_json.get("accounts", [])

    for account in accounts: # Iterate through the accounts and fetch transactions for each one
        account_id = account.get("account")
        account_name = account.get("customer")
        currency = account.get("currency")

        if not account_id or not account_name or not currency:
            continue

        transactions_response = fetch_transactions(jwt_token, account_id, start_date, end_date) # Fetch transactions for the account within the date range
        transactions = transactions_response.get("transactions", [])


        filtered_transactions = filter_transactions(transactions, account_id) # Filter and save the transactions to a CSV file
        save_transactions_to_csv(filtered_transactions, account_mapping.get(account_id, "Unknown"), currency)

if __name__ == "__main__":
    main()
