"""
This module contains the UserRepository class which interfaces with the MongoDB database.
It provides methods for retrieving and managing users, funds, subscriptions, and transactions
in the context of the application's business rules.
"""


class UserRepository:
    """
    This class provides an interface for interacting with MongoDB collections
    related to users, funds, subscriptions, and transactions. It encapsulates
    methods for querying, updating, and deleting documents in these collections,
    implementing the business rules of the application.
    """

    def __init__(self, db) -> None:
        """
        Initializes the UserRepository with a MongoDB client.

        Args:
            db: The MongoDB client instance that connects to the database.
        """
        self.db = db

    def has_active_subscription(self, user_id: str, fund_id: str) -> bool:
        """
        Checks if a user has an active subscription to a particular fund.

        Args:
            user_id: The unique ID of the user.
            fund_id: The unique ID of the fund.

        Returns:
            bool: True if the user has an active subscription to
                  the specified fund, False otherwise.
        """
        active_subscription = self.db.transactions.find_one(
            {"user_id": user_id, "fund_id": fund_id, "type": "subscription"}
        )
        return active_subscription is not None

    def find_unique_user(self):
        """
        Retrieves the only user from the 'users' collection.

        Returns:
            dict: The first and unique user document from the collection.
        """
        return self.db.users.find_one()

    def find_all_funds(self):
        """
        Retrieves all the funds from the 'funds' collection.

        Returns:
            list: A list of all fund documents in the collection.
        """
        return list(self.db.funds.find({}))

    def find_user(self, user_id: str):
        """
        Retrieves a user by their unique ID.

        Args:
            user_id: The unique ID of the user.

        Returns:
            dict: The user document if found, None otherwise.
        """
        return self.db.users.find_one({"_id": user_id})

    def find_fund(self, fund_id: str):
        """
        Retrieves a fund by its unique ID.

        Args:
            fund_id: The unique ID of the fund.

        Returns:
            dict: The fund document if found, None otherwise.
        """
        return self.db.funds.find_one({"_id": fund_id})

    def update_user_balance_and_transactions(
        self, user_id: str, amount: float, transaction
    ) -> None:
        """
        Updates the user's balance and logs the transaction in the 'transactions' collection.

        Args:
            user_id: The unique ID of the user.
            amount: The amount to be added or subtracted from the user's balance.
            transaction: The transaction document to be inserted into the 'transactions' collection.
        """
        self.db.users.update_one({"_id": user_id}, {"$inc": {"balance": amount}})
        self.db.transactions.insert_one(transaction)

    def add_subscription(self, subscription: dict) -> None:
        """
        Registers a new subscription in the 'subscriptions' collection.

        Args:
            subscription: A dictionary containing the subscription data.
        """
        self.db.subscriptions.insert_one(subscription)

    def find_last_subscription(self, user_id: str, fund_id: str):
        """
        Finds the most recent active subscription for a user and a specific fund.

        Args:
            user_id: The unique ID of the user.
            fund_id: The unique ID of the fund.

        Returns:
            dict: The most recent subscription document if found, None otherwise.
        """
        return self.db.subscriptions.find_one({"user_id": user_id, "fund_id": fund_id})

    def remove_subscription(self, subscription_id: str) -> None:
        """
        Removes an active subscription from the 'subscriptions' collection.

        Args:
            subscription_id: The unique ID of the subscription to be removed.
        """
        self.db.subscriptions.delete_one({"subscription_id": subscription_id})

    def add_transaction(self, transaction: dict) -> None:
        """
        Registers a transaction in the 'transactions' collection.

        Args:
            transaction: A dictionary containing the transaction data.
        """
        self.db.transactions.insert_one(transaction)

    def update_user_balance(self, user_id: str, amount: float) -> None:
        """
        Updates the user's balance in the 'users' collection.

        Args:
            user_id: The unique ID of the user.
            amount: The amount to add to or subtract from the user's balance.
        """
        self.db.users.update_one({"_id": user_id}, {"$inc": {"balance": amount}})

    def get_transactions(self, user_id: str):
        """
        Retrieves all transactions for a specific user from the 'transactions' collection.

        Args:
            user_id: The unique ID of the user.

        Returns:
            list: A list of transaction documents related to the user.
        """
        return list(self.db.transactions.find({"user_id": user_id}))
