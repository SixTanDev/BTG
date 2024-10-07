"""
Unit tests for the schemas and responses in the application.

This module contains tests for various schemas such
as FundSchema, UserSchema,  and response types including
SuccessResponse, ErrorResourceNotFound, and others.
"""

from application.schema_swagger import (
    FundSchema,
    SuccessResponse,
    ErrorResourceNotFound,
    TransactionSchema,
    UserSchema,
    ValidationErrorResponse,
    SubscriptionCreatedResponse,
    ConflictErrorResponse,
    BadRequestErrorResponse,
    CancellationSuccessResponse,
    NoActiveSubscriptionErrorResponse,
    TransactionHistorySuccessResponse,
    NoTransactionsFoundErrorResponse,
)


def test_fund_schema():
    """Test basic structure of FundSchema."""
    fund_data = {
        "_id": "fund123",
        "name": "Global Fund",
        "minimum_subscription": 1000,
        "category": "Equity",
    }
    fund = FundSchema(**fund_data)
    assert fund.name == "Global Fund"
    assert fund.minimum_subscription == 1000


def test_success_response():
    """Test basic structure of SuccessResponse."""
    response_data = {
        "status_code": 200,
        "value": [
            {
                "_id": "fund123",
                "name": "Global Fund",
                "minimum_subscription": 1000,
                "category": "Equity",
            }
        ],
    }
    response = SuccessResponse(**response_data)
    assert response.type == "Success"
    assert response.status_code == 200
    assert len(response.value) == 1


def test_error_resource_not_found():
    """Test basic structure of ErrorResourceNotFound."""
    error_data = {
        "type": "ResourceError",
        "status_code": 404,
        "message": "Resource not found.",
    }
    error = ErrorResourceNotFound(**error_data)
    assert error.status_code == 404
    assert error.message == "Resource not found."


def test_transaction_schema():
    """Test basic structure of TransactionSchema."""
    transaction_data = {
        "transaction_id": "trans123",
        "user_id": "user123",
        "fund_id": "fund123",
        "amount": 500.0,
        "type": "subscription",
        "date": "2024-01-01T12:00:00",
    }
    transaction = TransactionSchema(**transaction_data)
    assert transaction.amount == 500.0
    assert transaction.type == "subscription"


def test_user_schema():
    """Test basic structure of UserSchema."""
    user_data = {
        "_id": "user123",
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+123456789",
        "balance": 5000,
        "transactions": [],
        "notification_preference": ["email"],
    }
    user = UserSchema(**user_data)
    assert user.email == "john@example.com"
    assert user.balance == 5000


def test_validation_error_response():
    """Test structure of ValidationErrorResponse."""
    error_data = {
        "detail": [
            {
                "loc": ["body", "amount"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
    error_response = ValidationErrorResponse(**error_data)
    assert len(error_response.detail) == 1
    assert error_response.detail[0].msg == "field required"


def test_subscription_created_response():
    """Test structure of SubscriptionCreatedResponse."""
    response_data = {
        "type": "Created",
        "status_code": 201,
        "value": {"message": "Successful subscription to fund XYZ"},
    }
    response = SubscriptionCreatedResponse(**response_data)
    assert response.type == "Created"
    assert response.status_code == 201
    assert response.value == {"message": "Successful subscription to fund XYZ"}


def test_conflict_error_response():
    """Test structure of ConflictErrorResponse."""
    response_data = {
        "type": "ConflictError",
        "status_code": 409,
        "message": "You are already subscribed to fund XYZ.",
    }
    response = ConflictErrorResponse(**response_data)
    assert response.type == "ConflictError"
    assert response.status_code == 409
    assert "You are already subscribed" in response.message


def test_bad_request_error_response():
    """Test structure of BadRequestErrorResponse."""
    response_data = {
        "type": "ParametersError",
        "status_code": 400,
        "message": "Invalid amount",
    }
    response = BadRequestErrorResponse(**response_data)
    assert response.type == "ParametersError"
    assert response.status_code == 400
    assert response.message == "Invalid amount"


def test_cancellation_success_response():
    """Test structure of CancellationSuccessResponse."""
    response_data = {
        "type": "Success",
        "status_code": 201,
        "value": {"message": "Successful cancellation of subscription to fund XYZ"},
    }
    response = CancellationSuccessResponse(**response_data)
    assert response.type == "Success"
    assert response.status_code == 201
    assert response.value == {
        "message": "Successful cancellation of subscription to fund XYZ"
    }


def test_no_active_subscription_error_response():
    """Test structure of NoActiveSubscriptionErrorResponse."""
    response_data = {
        "type": "ParametersError",
        "status_code": 400,
        "message": "No active subscription found for fund XYZ",
    }
    response = NoActiveSubscriptionErrorResponse(**response_data)
    assert response.type == "ParametersError"
    assert response.status_code == 400
    assert "No active subscription found" in response.message


def test_transaction_history_success_response():
    """Test structure of TransactionHistorySuccessResponse."""
    response_data = {"type": "Success", "status_code": 200, "value": []}
    response = TransactionHistorySuccessResponse(**response_data)
    assert response.type == "Success"
    assert response.status_code == 200
    assert response.value == []


def test_no_transactions_found_error_response():
    """Test structure of NoTransactionsFoundErrorResponse."""
    response_data = {
        "type": "ResourceError",
        "status_code": 404,
        "message": "No transactions found for this user.",
    }
    response = NoTransactionsFoundErrorResponse(**response_data)
    assert response.type == "ResourceError"
    assert response.status_code == 404
    assert "No transactions found" in response.message
