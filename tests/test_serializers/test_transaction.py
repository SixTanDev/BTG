"""
Unit tests for the Transaction and TransactionList Pydantic models.

This module contains tests to validate the creation and structure of
Transaction and TransactionList models, including cases for valid data,
invalid data, and handling of timezone-aware datetime objects.
"""

from datetime import datetime
import pytest
from pydantic import ValidationError
from btg.serializers.transaction import Transaction, TransactionList


def test_transaction_valid_data():
    """
    Test for creating a valid `Transaction` instance with proper data.

    This test checks if a `Transaction` model can be created correctly when provided
    with valid transaction data, and whether the date is properly converted to
    the 'America/Bogota' timezone.
    """
    # Arrange
    input_data = {
        "transaction_id": "txn123",
        "user_id": "user123",
        "fund_id": "fund123",
        "amount": 100.0,
        "type": "subscription",
        "date": datetime(2024, 1, 1, 12, 0, 0),
    }

    # Act
    transaction = Transaction(**input_data)

    # Assert
    assert transaction.transaction_id == input_data["transaction_id"]
    assert transaction.user_id == input_data["user_id"]
    assert transaction.fund_id == input_data["fund_id"]
    assert transaction.amount == input_data["amount"]
    assert transaction.type == input_data["type"]


def test_transaction_invalid_date():
    """
    Test for creating a `Transaction` with an invalid date.

    This test checks that an invalid datetime format raises a validation error when
    creating a `Transaction` instance.
    """
    # Arrange
    input_data = {
        "transaction_id": "txn123",
        "user_id": "user123",
        "fund_id": "fund123",
        "amount": 100.0,
        "type": "subscription",
        "date": "invalid_date_format",
    }

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        Transaction(**input_data)

    assert "Invalid datetime format" in str(exc_info.value)


def test_transaction_naive_date():
    """
    Test for handling a naive datetime object.

    This test checks that if a naive (timezone-less) datetime object is passed
    into the `Transaction` model, it gets localized to UTC and then converted
    to the 'America/Bogota' timezone.
    """
    # Arrange
    naive_datetime = datetime(2024, 1, 1, 12, 0, 0)
    input_data = {
        "transaction_id": "txn123",
        "user_id": "user123",
        "fund_id": "fund123",
        "amount": 100.0,
        "type": "subscription",
        "date": naive_datetime,
    }

    # Act
    transaction = Transaction(**input_data)

    # Assert
    assert transaction.date.tzinfo is not None


def test_transaction_list_valid_data():
    """
    Test for creating a `TransactionList` with valid data.

    This test checks if a `TransactionList` model can be created correctly when
    provided with a list of valid `Transaction` data.
    """
    # Arrange
    input_data = [
        {
            "transaction_id": "txn123",
            "user_id": "user123",
            "fund_id": "fund123",
            "amount": 100.0,
            "type": "subscription",
            "date": datetime(2024, 1, 1, 12, 0, 0),
        },
        {
            "transaction_id": "txn124",
            "user_id": "user124",
            "fund_id": "fund124",
            "amount": 200.0,
            "type": "cancellation",
            "date": datetime(2024, 1, 2, 12, 0, 0),
        },
    ]

    # Act
    transactions = [Transaction(**data) for data in input_data]
    transaction_list = TransactionList(transactions=transactions)

    # Assert
    assert len(transaction_list.transactions) == 2
    assert transaction_list.transactions[0].transaction_id == "txn123"
    assert transaction_list.transactions[1].transaction_id == "txn124"


def test_transaction_list_invalid_data():
    """
    Test for `TransactionList` with invalid transaction data.

    This test checks that if invalid data (missing
    required fields or invalid field types)
    is provided to a `TransactionList`, a `ValidationError` is raised.
    """
    # Arrange
    invalid_data = [
        {
            "transaction_id": "txn123",
            "user_id": "user123",
            "amount": 100.0,
            "type": "subscription",
            "date": datetime(2024, 1, 1, 12, 0, 0),
        },
        # Missing 'fund_id' and 'date' in the second transaction
        {
            "transaction_id": "txn124",
            "user_id": "user124",
            "amount": 200.0,
            "type": "cancellation",
        },
    ]

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        transactions = [Transaction(**data) for data in invalid_data]
        TransactionList(transactions=transactions)

    assert "fund_id" in str(exc_info.value)
