# DESIGN.md

## Design Document for Automated Bank Transactions Upload System

## High-Level Architecture
The system comprises the following core components:
1. **Bank Frick Connector (`bankfrick_connect.py`)**: Handles secure authentication with Bank Frick’s API using RSA keys.
2. **Transaction Fetcher (`fetch_transactions.py`, `fetch_daily.py`)**: Responsible for retrieving transaction data from Bank Frick’s API within specific timeframes.
3. **Data Processor (`fetch_daily_summary.py`)**: Summarizes daily transaction activity to provide insights into financial operations.
4. **Iplicit Connector (`iplicit_connector.py`, `fetch_post_transactions.py`)**: Prepares and transmits transactions to Iplicit’s API. However, while the posting logic is functional, the transactions are not reflecting on Iplicit’s end, necessitating further troubleshooting. Queries have been raised with Iplicit’s support team, and their response is awaited.

## Workflow
1. **Authentication Process**:
   - The system securely authenticates with Bank Frick’s API using JWT tokens created via RSA signatures. This is managed by `bankfrick_connect.py`.
2. **Transaction Retrieval**:
   - Daily transactions are fetched using `fetch_daily.py`.
   - Weekly data or custom date ranges are fetched via `fetch_transactions.py`.
3. **Transaction Summary**:
   - Before running other scripts, `fetch_daily_summary.py` can be used to check for transaction availability, saving unnecessary effort.
4. **Data Formatting**:
   - Transactions are categorized, formatted, and saved as CSV files for downstream processing.
5. **Posting to Iplicit**:
   - `iplicit_connector.py` and `fetch_post_transactions.py` handle formatting and posting of transactions to the Iplicit API.

## Component Breakdown
1. **`bankfrick_connect.py`**:
   - Generates JWT tokens using RSA private keys for secure API communication with Bank Frick.
   - Handles key-related errors and ensures secure communication.

2. **`fetch_transactions.py`**:
   - Fetches transactions from Bank Frick’s API for specific accounts and date ranges.
   - Saves transactions to CSV files for manual processing if needed.

3. **`fetch_daily.py`**:
   - A simplified version of `fetch_transactions.py`, designed to retrieve transactions for the previous day.
   - Primarily used for daily operations.

4. **`fetch_daily_summary.py`**:
   - Summarizes transaction data for the previous day to determine if further scripts need to be run.
   - Outputs clear logs indicating transaction activity for each account.

5. **`iplicit_connector.py`**:
   - Formats and posts transactions to the Iplicit API.
   - Logs successful and failed attempts for debugging.

6. **`fetch_post_transactions.py`**:
   - Combines transaction fetching and posting in one workflow.
   - Useful for monthly reconciliations or bulk operations.

## Design Decisions
1. **Modular Design**:
   - Each script performs a specific function, ensuring maintainability and scalability.
   - This allows individual components to be tested and improved independently.

2. **CSV as an Interim Format**:
   - Chosen to provide a manual fallback for scenarios where API integration with Iplicit is incomplete.
   - Simplifies data validation and debugging.

3. **Secure Authentication**:
   - RSA keys and JWT tokens ensure secure communication with Bank Frick’s API.
   - Private keys are excluded from production environments for security.

## Implementation Challenges
1. **Iplicit API Delays**:
   - The integration with Iplicit is incomplete due to delays in support and lack of clear documentation.
   - CSV exports are used as a workaround for manual uploads.

2. **RSA Key Setup**:
   - Configuring RSA keys for Bank Frick’s API required careful attention to file formats and permissions.

3. **Error Handling**:
   - Comprehensive error handling is implemented for API communication, but more robust logging and retry mechanisms are planned for future versions.

## Future Enhancements
1. **Full Automation**:
   - Complete the integration with Iplicit’s API to enable end-to-end automation without manual intervention.

2. **Cloud Deployment**:
   - Deploy the system on cloud platforms (e.g., AWS Lambda) for continuous and scalable operation.

3. **Real-Time Notifications**:
   - Implement email or Slack notifications for critical errors and transaction updates.

4. **Advanced Monitoring**:
   - Develop a web-based dashboard to track transaction statuses, summaries, and system health.

5. **Improved Error Handling**:
   - Add retry mechanisms and detailed error logs for API communication issues.

## Key Takeaways
- **Importance of Modularity**:
   - Splitting functionality into distinct scripts made the project easier to develop and debug.
- **Balancing Automation and Manual Fallbacks**:
   - The use of CSV exports ensures the system remains functional even during API integration issues.
- **Incremental Development**:
   - The modular approach allowed steady progress and paved the way for future enhancements.

---

The Automated Bank Transactions Upload System is a robust solution for streamlining financial workflows. It reduces manual intervention, improves accuracy, and lays the foundation for further automation and scalability.
