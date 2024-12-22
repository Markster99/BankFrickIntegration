import requests
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# Configuration settings for connecting to the Bank Frick API
BASE_URL = "https://olb.bankfrick.li/webapi/v2"  # Bank Frick API URL
AUTH_ENDPOINT = "/authorize" # Bank Frick Endpoint to obtain the JWT token
API_KEY = "Placheolder"  # Will make this connect to a 2nd file to make it privat
PRIVATE_KEY_PATH = "Placheolder"  # Path to private key

def generate_signature(payload: str, private_key_path: str) -> str:
    """
    Generate a signature for the given payload using my private key.
    """
    try:
        # Load up my private key
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None  # Should really make it have a password for securty but do that in future
            )

        # Generate the RSA signature
        signature = private_key.sign(
            payload.encode("utf-8"),  # Convert the payload to bytes
            padding.PKCS1v15(),
            hashes.SHA512()
        )

        # Encode the signature in base64 to send across
        return base64.b64encode(signature).decode("utf-8")
    except Exception as e:
        # Log the error and exit if the signing process fails
        print(f"Error during signature generation: {e}")
        exit(1)

def get_jwt_token():
    """
    Request a JWT token from the server using the API-Key and RSA signature from my private key.
    """
    url = f"{BASE_URL}{AUTH_ENDPOINT}" # Make the URL for the authorization endpoint
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = {"key": API_KEY}
    payload_json = json.dumps(payload)

    # Generate signature for payload
    signature = generate_signature(payload_json, PRIVATE_KEY_PATH)

    # Add the signature and algorithm details to the headers
    headers["Signature"] = signature
    headers["algorithm"] = "rsa-sha512"

    print(f"Payload JSON: {payload_json}")
    print("Requesting JWT token...")
    try:
        response = requests.post(url, headers=headers, data=payload_json)

        if response.status_code == 200: # working
            print("JWT token received successfully.")
            return response.json().get("token")
        else: # problem
            print(f"Failed to fetch JWT token: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        exit(1)

if __name__ == "__main__":
    # Main entry point to request and display the JWT token
    token = get_jwt_token()
    if token:
        print(f"JWT Token: {token}")
    else:
        print("JWT Token could not be retrieved.")
