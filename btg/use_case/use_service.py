"""
This module implements the use cases for our technical test.

It contains the logic for managing user subscriptions, fund management,
transaction history retrieval, and other related business operations.
All operations interact with MongoDB through the UserRepository.
The responses are standardized using ResponseSuccess and ResponseFailure.
"""

# pylint: disable=E0401, E0611, W0718, R0911

from datetime import datetime
import pytz
import uuid
from btg.repository.user_repository import UserRepository
from btg.response import ResponseSuccess, ResponseFailure, ResponseTypes
from btg.serializers.transaction import TransactionList


# Notification simulations
def send_email(email, message):
    """
    This is a placeholder function for sending email notifications.
    This is not the final implementation and should be replaced by a proper
    email sending service (e.g., SMTP, a third-party service like SendGrid).

    Args:
        email (str): The recipient's email address.
        message (str): The message to send to the recipient.
    """
    print(f"Sending email to {email}: {message}")


def send_sms(phone, message):
    """
    This is a placeholder function for sending SMS notifications.
    This is not the final implementation and should be replaced by a proper
    SMS service (e.g., Twilio, Nexmo, etc.).

    Args:
        phone (str): The recipient's phone number.
        message (str): The message to send to the recipient.
    """
    print(f"Sending SMS to {phone}: {message}")


class UserService:
    """
    This service class handles operations related to user subscriptions, fund management,
    and transaction history. It interacts with the UserRepository to perform actions
    such as subscribing to a fund, canceling a subscription, and retrieving transaction history.
    """

    def __init__(self, db) -> None:
        """
        Initializes the UserService with a MongoDB client instance.

        Args:
            db: The MongoDB client instance used to interact with the database.
        """
        self.repository = UserRepository(db=db)

    def get_all_funds(self) -> ResponseSuccess | ResponseFailure:
        """
        Retrieves all available funds from the database.

        Verifies that the list of funds is not empty. If no funds are found,
        returns a system error since there should be funds available.

        Returns:
            ResponseSuccess: Contains the list of funds if funds are available.
            ResponseFailure: Returns a system error if no funds are found.
        """
        funds = self.repository.find_all_funds()
        if not funds:
            return ResponseFailure(
                type_=ResponseTypes.SYSTEM_ERROR,
                message="No funds available in the system.",
            )
        return ResponseSuccess(value=funds)

    def get_user_info(self) -> ResponseSuccess | ResponseFailure:
        """
        Retrieves the unique user information from the database.

        Returns:
            ResponseSuccess: If the user is found, returns the user information.
            ResponseFailure: If no user is found, returns an error message.
        """
        user = self.repository.find_unique_user()
        if not user:
            return ResponseFailure(
                type_=ResponseTypes.RESOURCE_ERROR, message="User not found"
            )

        transactions = self.repository.get_transactions(user["_id"])
        user["transactions"] = TransactionList(transactions=transactions).transactions

        return ResponseSuccess(value=user)

    def subscribe_to_fund(
        self, user_id: str, fund_id: str, amount: float
    ) -> ResponseSuccess | ResponseFailure:
        """
        Handles the process of subscribing a user to a fund, including verifying
        the user's balance and the fund's requirements, registering the subscription,
        and updating the user's balance.

        Args:
            user_id (str): The unique identifier for the user.
            fund_id (str): The unique identifier for the fund.
            amount (float): The amount to be subscribed.

        Returns:
            ResponseSuccess: If the subscription is successful.
            ResponseFailure: If the subscription fails due to insufficient balance,
                             already active subscription, or other validation issues.
        """
        user = self.repository.find_user(user_id)
        if not user:
            return ResponseFailure(
                type_=ResponseTypes.RESOURCE_ERROR, message="User not found"
            )

        fund = self.repository.find_fund(fund_id)
        if not fund:
            return ResponseFailure(
                type_=ResponseTypes.RESOURCE_ERROR,
                message=f"Fund {fund_id} does not exist.",
            )

        if self.repository.find_last_subscription(user_id, fund_id):
            message: str = (
                f"You are already subscribed to fund {fund['name']}. You must cancel your "
                f"subscription before subscribing again."
            )
            return ResponseFailure(type_=ResponseTypes.CONFLICT_ERROR, message=message)

        if amount > user["balance"]:
            message: str = (
                f"The amount you tried to subscribe ({amount:.2f}) is greater than your available "
                f"balance ({user['balance']:.2f}). "
                f"The value of the fund {fund['name']} is {fund['minimum_subscription']:.2f}, "
                f"you must adjust the subscription to the amount of the fund."
            )
            return ResponseFailure(
                type_=ResponseTypes.PARAMETERS_ERROR, message=message
            )
        if amount < fund["minimum_subscription"]:
            message: str = (
                f"The minimum amount to subscribe to the fund {fund['name']} is "
                f"{fund['minimum_subscription']:.2f}."
            )
            return ResponseFailure(
                type_=ResponseTypes.PARAMETERS_ERROR, message=message
            )

        # Define the time zone of Colombia
        timezone_colombia = pytz.timezone('America/Bogota')

        subscription = {
            "subscription_id": str(uuid.uuid4()),
            "user_id": user_id,
            "fund_id": fund_id,
            "amount": amount,
            "date": datetime.now(timezone_colombia),
        }

        try:
            self.repository.add_subscription(subscription)

            transaction = {
                "transaction_id": str(uuid.uuid4()),
                "user_id": user_id,
                "fund_id": fund_id,
                "amount": amount,
                "type": "subscription",
                "date": datetime.now(timezone_colombia)
            }

            self.repository.add_transaction(transaction)
            self.repository.update_user_balance(user_id, -amount)

            self._send_notifications(
                user=user,
                message=f"You have subscribed to fund {fund['name']} for {amount}.",
            )

            return ResponseSuccess(
                value=f"Successful subscription to fund {fund['name']}",
                response_type=ResponseTypes.CREATED,
            )
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, str(e))

    def _find_funds_within_amount(self, user, amount):
        """
        Finds funds that the user can subscribe to based on the amount they are willing to invest.

        Args:
            user (dict): The user object containing their current transactions.
            amount (float): The amount the user wants to invest.

        Returns:
            list: A list of funds the user can subscribe to.
        """
        funds = self.repository.find_all_funds()

        active_fund_ids = {
            txn["fund_id"]
            for txn in user["transactions"]
            if txn["type"] == "subscription"
            and not any(
                c["fund_id"] == txn["fund_id"] and c["type"] == "cancellation"
                for c in user["transactions"]
            )
        }

        available_funds = [
            fund
            for fund in funds
            if fund["minimum_subscription"] <= amount
            and fund["_id"] not in active_fund_ids
        ]

        return available_funds

    def _find_funds_within_balance(self, balance):
        """
        Finds funds the user can subscribe to based on their current balance.

        Args:
            balance (float): The user's current balance.

        Returns:
            list: A list of funds the user can afford to subscribe to.
        """
        funds = self.repository.find_all_funds()
        return [fund for fund in funds if fund["minimum_subscription"] <= balance]

    def cancel_subscription(
        self, user_id: str, fund_id: str
    ) -> ResponseSuccess | ResponseFailure:
        """
        Cancels the user's active subscription to a specific fund and refunds the amount.

        Args:
            user_id (str): The unique identifier for the user.
            fund_id (str): The unique identifier for the fund.

        Returns:
            ResponseSuccess: If the cancellation is successful.
            ResponseFailure: If the cancellation fails, either due to the user not being
                             subscribed to the fund or other issues.
        """
        user = self.repository.find_user(user_id)
        if not user:
            return ResponseFailure(
                type_=ResponseTypes.RESOURCE_ERROR, message="User not found"
            )

        fund = self.repository.find_fund(fund_id)
        if not fund:
            return ResponseFailure(
                type_=ResponseTypes.RESOURCE_ERROR,
                message=f"Fund {fund_id} does not exist.",
            )

        active_subscription = self.repository.find_last_subscription(user_id, fund_id)
        if not active_subscription:
            message = f"No active subscription found for fund {fund['name']}"
            return ResponseFailure(
                type_=ResponseTypes.PARAMETERS_ERROR, message=message
            )

        # Define the time zone of Colombia
        timezone_colombia = pytz.timezone('America/Bogota')

        cancellation = {
            "transaction_id": str(uuid.uuid4()),
            "user_id": user_id,
            "fund_id": fund_id,
            "amount": active_subscription["amount"],
            "type": "cancellation",
            "subscription_id": active_subscription["subscription_id"],
            "date": datetime.now(timezone_colombia),
        }

        try:
            self.repository.add_transaction(cancellation)
            self.repository.remove_subscription(active_subscription["subscription_id"])
            self.repository.update_user_balance(user_id, active_subscription["amount"])

            self._send_notifications(
                user=user,
                message=(
                    f"You have cancelled your subscription to fund {fund['name']} and "
                    f"have been refunded {active_subscription['amount']}."
                ),
            )

            return ResponseSuccess(
                value=f"Successful cancellation of subscription to fund {fund['name']}",
                response_type=ResponseTypes.CREATED,
            )
        except Exception as e:
            return ResponseFailure(type_=ResponseTypes.SYSTEM_ERROR, message=str(e))

    def get_transaction_history(
        self, user_id: str
    ) -> ResponseSuccess | ResponseFailure:
        """
        Retrieves the transaction history of a user.

        Args:
            user_id (str): The unique identifier for the user.

        Returns:
            ResponseSuccess: If transactions are found, returns the list of transactions.
            ResponseFailure: If no transactions are found or the user does not exist.
        """
        user = self.repository.find_user(user_id)
        if not user:
            return ResponseFailure(
                type_=ResponseTypes.RESOURCE_ERROR, message="User not found"
            )

        transactions = self.repository.get_transactions(user_id)
        if not transactions:
            return ResponseFailure(
                type_=ResponseTypes.RESOURCE_ERROR,
                message="No transactions found for this user.",
            )

        return ResponseSuccess(
            value=TransactionList(transactions=transactions).transactions
        )

    def _send_notifications(self, user, message):
        """
        Sends notifications to the user based on their preferences.

        Args:
            user (dict): The user object containing notification preferences.
            message (str): The message to be sent to the user.
        """
        if "email" in user["notification_preference"]:
            send_email(user["email"], message)
        if "sms" in user["notification_preference"]:
            send_sms(user["phone"], message)
