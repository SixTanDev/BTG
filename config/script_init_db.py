"""
This script initializes the MongoDB database
with initial data for the application.

It creates a new user with a specified initial
balance and inserts a predefined set of funds into the
'funds' collection. This setup is essential for the application
to function correctly, providing baseline data for
testing or development purposes.
"""

import uuid
from pymongo import MongoClient


# Connect to MongoDB instance running in Docker
client = MongoClient(
    "mongodb://root:example@mongodb:27017/"
)  # Ensure this matches your Docker configuration
db = client["btg_db"]  # Connect or create the 'btg_db' database

# Define business rules for initial setup
INITIAL_BALANCE = 500000  # Initial balance assigned to the new user

# Create a new user with a unique ID and initial balance
new_user = {
    "_id": str(uuid.uuid4()),  # Generate a unique identifier for the user
    "name": "Emmanuel",
    "email": "sixtandev@gmail.com",
    "phone": "+573043543065",
    "balance": INITIAL_BALANCE,  # Assign the user's starting balance
    "transactions": [],  # Initialize an empty transaction history
    "notification_preference": [
        "email",
        "sms",
    ],  # User prefers notifications via email and SMS
}

# Insert the new user into the 'users' collection within the database
db.users.insert_one(new_user)


# Define a set of funds available for subscription
funds_data = [
    {
        "_id": "fund_1",
        "name": "FPV_BTG_PACTUAL_RECAUDADORA",
        "minimum_subscription": 75000,
        "category": "FPV",
    },
    {
        "_id": "fund_2",
        "name": "FPV_BTG_PACTUAL_ECOPETROL",
        "minimum_subscription": 125000,
        "category": "FPV",
    },
    {
        "_id": "fund_3",
        "name": "DEUDAPRIVADA",
        "minimum_subscription": 50000,
        "category": "FIC",  # Fixed Income Category
    },
    {
        "_id": "fund_4",
        "name": "FDO-ACCIONES",
        "minimum_subscription": 250000,
        "category": "FIC",
    },
    {
        "_id": "fund_5",
        "name": "FPV_BTG_PACTUAL_DINAMICA",
        "minimum_subscription": 100000,
        "category": "FPV",
    },
]

# Insert the funds into the 'funds' collection within the database
result = db.funds.insert_many(funds_data)
print("Funds inserted:", result.inserted_ids)  # Print the IDs of the inserted funds
