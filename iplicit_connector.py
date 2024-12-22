import requests
import json

def post_transaction_to_iplicit(api_key, transaction_payload):
    """
    Post a single transaction to Iplicit.
    """
    url = "https://api.iplicit.com/BankTransaction"  # BankTransaction endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.post(url, headers=headers, json=transaction_payload)
        if response.status_code in [200, 201]:
            print(f"Successfully posted transaction: {transaction_payload['Reference']}")
            return response.json()
        else:
            print(f"Failed to post transaction. Status: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error posting transaction: {str(e)}")
        return None

def build_transaction_payload(legal_entity, bank_account, code, date, amount, description):
    """
    Build the payload required for the Iplicit API.
    """
    return {
        "LegalEntity": legal_entity,
        "BankAccount": bank_account,
        "Code": code,
        "TransactionDate": date,
        "Amount": amount,
        "Reference": description,
        "Description": description
    }
