"""
This module contains Pydantic schemas used to enhance Swagger UI documentation
in the FastAPI application. These schemas define the structure of request and
response models for various API endpoints, facilitating better documentation
and validation.
"""

from typing import List, Union, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class FundSchema(BaseModel):
    """
    Represents a fund with its basic details.
    """

    _id: str
    name: str
    minimum_subscription: int
    category: str


class SuccessResponse(BaseModel):
    """
    Represents a generic success response.
    """

    type: str = "Success"
    status_code: int
    value: List[FundSchema]


class ErrorResourceNotFound(BaseModel):
    """
    Represents an error response when a resource is not found.
    """

    type: str
    status_code: int
    message: str


class TransactionSchema(BaseModel):
    """
    Represents a transaction with its details.
    """

    transaction_id: str
    user_id: str
    fund_id: str
    amount: float
    type: str
    date: datetime


class UserSchema(BaseModel):
    """
    Represents a user with their details.
    """

    _id: str
    name: str
    email: str
    phone: str
    balance: int
    transactions: List[TransactionSchema]
    notification_preference: List[str]


class ValidationErrorDetail(BaseModel):
    """
    Represents a single validation error detail.
    """

    loc: List[Union[str, int]]
    msg: str
    type: str


class ValidationErrorResponse(BaseModel):
    """
    Represents a response containing multiple validation errors.
    """

    detail: List[ValidationErrorDetail]


class SubscriptionCreatedResponse(BaseModel):
    """
    Represents a successful response when a subscription is created.
    """

    type: Literal["Created"]
    status_code: Literal[201]
    value: dict = Field(
        default="Successful subscription to fund XYZ",
        description="A message indicating successful creation of the subscription.",
    )


class ConflictErrorResponse(BaseModel):
    """
    Represents an error response due to a conflict, such as an existing subscription.
    """

    type: Literal["ConflictError"]
    status_code: Literal[409]
    message: str = Field(
        default=(
            "You are already subscribed to fund XYZ. You must "
            "cancel your subscription before subscribing again."
        ),
        description="A message indicating a conflict due to an existing subscription.",
    )


class BadRequestErrorResponse(BaseModel):
    """
    Represents a bad request error response due to invalid parameters.
    """

    type: Literal["ParametersError"]
    status_code: Literal[400]
    message: str = Field(
        default=...,
        example=(
            "The amount you tried to subscribe (5000000.00) is "
            "greater than your available balance (20000.00)."
        ),
        description="A message indicating a bad request due to invalid parameters.",
    )


class CancellationSuccessResponse(BaseModel):
    """
    Represents a successful response when a subscription is cancelled.
    """

    type: Literal["Success"]
    status_code: Literal[201]
    value: dict = Field(
        default="Successful cancellation of subscription to fund XYZ",
        description="A message indicating successful cancellation of the subscription.",
    )


class NoActiveSubscriptionErrorResponse(BaseModel):
    """
    Represents an error response when there is no active subscription to cancel.
    """

    type: Literal["ParametersError"]
    status_code: Literal[400]
    message: str = Field(
        default="No active subscription found for fund XYZ",
        description=(
            "A message indicating that there is no " "active subscription to cancel."
        ),
    )


class TransactionHistorySuccessResponse(BaseModel):
    """
    Represents a successful response containing the transaction history of a user.
    """

    type: Literal["Success"]
    status_code: Literal[200]
    value: List[TransactionSchema] = Field(
        default=..., description="A list of transactions belonging to the user."
    )


class NoTransactionsFoundErrorResponse(BaseModel):
    """
    Represents an error response when no transactions are found for a user.
    """

    type: Literal["ResourceError"]
    status_code: Literal[404]
    message: str = Field(
        default="No transactions found for this user.",
        description="A message indicating that the user has no transactions.",
    )
