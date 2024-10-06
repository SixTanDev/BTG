"""
This module contains serializers for transaction data using Pydantic models.

The `Transaction` model represents a single transaction, while the `TransactionList`
model handles a list of transactions. These serializers facilitate the conversion of
MongoDB documents into Python objects and ensure proper validation of the transaction data.
The models can also easily convert Python objects into JSON format, making it easier
to work with transaction data in web applications.
"""

# pylint: disable=R0903

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, field_validator
import pytz


class Transaction(BaseModel):
    """
    A Pydantic model representing a transaction, which could
    either be a subscription or a cancellation.
    This model is used to standardize and validate transaction data.
    """

    transaction_id: str
    user_id: str
    fund_id: str
    amount: float
    type: str  # "subscription" or "cancellation"
    date: datetime
    _id: Optional[str] = None  # To handle MongoDB ObjectId

    @field_validator("date", mode="before")
    def set_timezone(cls, v):
        if isinstance(v, datetime):
            if v.tzinfo is None:
                utc = pytz.utc
                v = utc.localize(v)
            colombia_tz = pytz.timezone("America/Bogota")
            return v.astimezone(colombia_tz)
        raise ValueError("Invalid datetime format")


class TransactionList(BaseModel):
    """
    A Pydantic model that represents a list of transactions.
    This model is used to validate and group multiple
    transactions into a single object for easier management.
    """

    transactions: List[Transaction]

    class Config:
        """
        Configuration for the Pydantic model.

        Attributes:
            arbitrary_types_allowed (bool): Allows Pydantic to accept types that are
                                            not natively supported,
            such as MongoDB's ObjectId.
        """

        arbitrary_types_allowed = True
