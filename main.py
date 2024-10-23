import sqlite3
import random

# Database setup - SQLite (a proxy for MS SQL)
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create claims table
cursor.execute('''CREATE TABLE claims (
                    claim_id INTEGER PRIMARY KEY,
                    customer_name TEXT NOT NULL,
                    policy_number TEXT NOT NULL,
                    claim_amount REAL NOT NULL,
                    claim_status TEXT NOT NULL CHECK(claim_status IN ('Pending', 'Approved', 'Rejected'))
                )''')

# Sample claims data
claims_data = [
    ('John Doe', 'PN12345', 2500.00, 'Pending'),
    ('Jane Smith', 'PN54321', 4000.00, 'Approved'),
    ('Chris Lee', 'PN67890', 3000.00, 'Pending')
]

# Insert sample data
cursor.executemany('''INSERT INTO claims (customer_name, policy_number, claim_amount, claim_status)
                      VALUES (?, ?, ?, ?)''', claims_data)
conn.commit()

# Function to validate claims - a proxy for improving data validation process
def validate_claims():
    # Fetch pending claims for processing
    cursor.execute("SELECT * FROM claims WHERE claim_status='Pending'")
    pending_claims = cursor.fetchall()

    print("Pending Claims Validation:")
    for claim in pending_claims:
        claim_id, customer_name, policy_number, claim_amount, claim_status = claim
        print(f"Processing Claim ID: {claim_id}")
        
        # Validate policy number format
        if not policy_number.startswith('PN'):
            print(f"Error: Invalid policy number format for {customer_name}")
            cursor.execute("UPDATE claims SET claim_status='Rejected' WHERE claim_id=?", (claim_id,))
        else:
            # Simulate external API validation for claim approval
            if api_validate_claim(claim_amount):
                print(f"Claim for {customer_name} is approved.")
                cursor.execute("UPDATE claims SET claim_status='Approved' WHERE claim_id=?", (claim_id,))
            else:
                print(f"Claim for {customer_name} is rejected.")
                cursor.execute("UPDATE claims SET claim_status='Rejected' WHERE claim_id=?", (claim_id,))
    
    conn.commit()

# Simulate API call for validating claims
def api_validate_claim(claim_amount):
    # Assume an external system approves claims below $3500
    return claim_amount < 3500

# Display claims after validation
def display_claims():
    cursor.execute("SELECT * FROM claims")
    all_claims = cursor.fetchall()

    print("\nAll Claims:")
    for claim in all_claims:
        claim_id, customer_name, policy_number, claim_amount, claim_status = claim
        print(f"Claim ID: {claim_id}, Customer: {customer_name}, Status: {claim_status}")

# Initial display of claims
display_claims()

# Validate claims process (improves manual data checks)
validate_claims()

# Display updated claims
display_claims()

# Close the connection
conn.close()
