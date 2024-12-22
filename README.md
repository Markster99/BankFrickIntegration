# README.md

## Automated Bank Transactions Upload System

### Overview
The Automated Bank Transactions Upload System is a tool developed to save time for me by streamlining the retrieval of bank transactions from Bank Frick’s API and formatting them for the Iplicit accounting system. While full automation with Iplicit is still under development, the system already provides significant time-saving functionalities for me and ensures greater accuracy in managing transactions.

Normally, this process would require logging into Bank Frick, going through each of the nine accounts one by one, filtering transactions by date, downloading them as CSV files, manually modifying their structure, and then importing them into Iplicit. Now, I can simply run a script to fetch the transactions and prepare them for upload, eliminating the repetitive, time-consuming chore and allowing for me to focus on more strategic tasks.

### Features
1. **Transaction Retrieval**: Automatically retrieve bank transaction data for the previous day or week from Bank Frick’s API.
2. **Transaction Summary**: Run the `fetch_daily_summary.py` script to quickly see if there are any transactions to process before deciding whether to run the full transaction download scripts. It saves me unnecessary effort when there are no new transactions.
3. **Automated Summaries**: Generate concise daily transaction summaries to quickly assess financial movements.
4. **CSV Export**: Export transactions in a structured format compatible with accounting workflows.
5. **Scalable Architecture**: Designed for seamless integration with the Iplicit API in the future.
6. **Error Handling and Logging**: Identifies and records issues to assist in maintaining data accuracy and facilitate resolution of issues.

### Installation
1. Extract the provided ZIP file to your desired directory.

2. Ensure you have Python 3.7 or higher installed on your system.

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the following files:
   - Update API keys in `bankfrick_connect.py` and `iplicit_connector.py`. (Note: The API keys are currently hardcoded to save time during development. After the presentation on Tuesday, these keys will be deleted, and the project will be refactored to use environment variables for security.)
   - Set the `PRIVATE_KEY_PATH` in `bankfrick_connect.py` to your private key location.

### Usage
1. **Fetch Daily Transactions**:
   ```bash
   python fetch_daily.py
   ```

   This script retrieves transactions from the previous day and generates a summary for review.

2. **Fetch Weekly Transactions**:
   ```bash
   python fetch_transactions.py
   ```

   Use this script to retrieve a week’s worth of transactions and save them as CSV files for further processing.

3. **Generate Daily Summary**:
   ```bash
   python fetch_daily_summary.py
   ```
   Use this script to check if there are any transactions for the previous day. This allows you to decide whether or not to proceed with running other scripts to fetch or process transactions.

4. **Post Transactions to Iplicit**:
   While the script (`fetch_post_transactions.py`) is operational and posts data to Iplicit, the transactions are currently not reflecting on Iplicit’s side. Further debugging is ongoing to resolve this issue, and queries have been sent to Iplicit’s API support team for clarification.

### Challenges
1. **Iplicit API Integration**: Integration with Iplicit’s API was delayed due to incomplete documentation. As a workaround, intermediate CSV exports were implemented for manual uploads.
2. **RSA Key Management**: Setting up RSA signatures required careful configuration of private keys.

### Security Notes
- API keys and private keys are currently hardcoded for development purposes but should be secured in a production environment.
- Future versions will use environment variables or a secret manager to handle sensitive credentials securely.

### Known Limitations
- Transactions posted to Iplicit do not appear immediately due to unresolved API integration issues.
- The system assumes all accounts follow the same structure; further testing may be required for edge cases.

### Future Developments
1. Complete the integration with Iplicit’s API to enable fully automated workflows.
2. Resolve the issue causing posted transactions to not appear in Iplicit.
3. Introduce email notifications for critical system errors to keep me informed.
4. Deploy the system on a cloud platform for continuous operation and scalability.
5. Optimize performance with caching mechanisms to reduce response times.

### Credits
- `requests` library for handling API calls.
- Bank Frick and Iplicit API documentation for integration details.
