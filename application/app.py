"""
This module defines the FastAPI application and its endpoints
for managing fund subscriptions, cancellations, and transaction history.
It includes the following endpoints:

1. Subscribe to a new fund.
2. Cancel an existing fund subscription.
3. View the history of recent transactions (subscriptions and cancellations).
4. Send notifications via email or SMS based on user preferences
   after subscribing to a fund.
"""

# pylint: disable=E0401, E0611

from typing import Union
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from btg.use_case.use_service import UserService
from btg.response import ResponseSuccess, ResponseFailure
from .schema_swagger import (
    SuccessResponse,
    ErrorResourceNotFound,
    UserSchema,
    ValidationErrorResponse,
    BadRequestErrorResponse,
    ConflictErrorResponse,
    SubscriptionCreatedResponse,
    CancellationSuccessResponse,
    NoActiveSubscriptionErrorResponse,
    TransactionHistorySuccessResponse,
    NoTransactionsFoundErrorResponse,
)

# MongoDB Connection
client = MongoClient("mongodb://root:example@btg_mongodb:27017/")
db = client["btg_db"]

app = FastAPI()


@app.get(path="/", include_in_schema=False)
def root():
    """
    **Root Endpoint**

    Redirects the user to the Swagger documentation page.

    **Returns**:
    - **RedirectResponse**: Redirects to the `/docs` Swagger UI.
    """
    return RedirectResponse(url="/docs")


@app.get(
    path="/funds",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResourceNotFound,
            "description": "Internal Server Error",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ValidationErrorResponse,
            "description": "Validation Error",
        },
    },
)
def get_all_funds():
    """
    **Get All Funds**

    Retrieve all funds available in the system.

    **Returns**:
    - **dict**: A dictionary containing a list of funds.
    """
    service: UserService = UserService(db)
    funds: ResponseSuccess | ResponseFailure = service.get_all_funds()

    return JSONResponse(content=jsonable_encoder(funds), status_code=funds.status_code)


@app.get(
    path="/user",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResourceNotFound,
            "description": "User Not Found",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ValidationErrorResponse,
            "description": "Validation Error",
        },
    },
)
def get_user():
    """
    **Get User Information**

    Retrieve information about a single user from the database.

    If the user is not found, a 'User Not Found' message is returned.

    **Returns**:
    - **dict**: User information or an error message.
    """
    service: UserService = UserService(db=db)
    user_info: ResponseSuccess | ResponseFailure = service.get_user_info()

    return JSONResponse(
        content=jsonable_encoder(user_info), status_code=user_info.status_code
    )


@app.post(
    path="/subscribe/{user_id}/{fund_id}/{amount}",
    response_model=SubscriptionCreatedResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": BadRequestErrorResponse,
            "description": "Bad Request due to invalid parameters.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ConflictErrorResponse,
            "description": "Conflict error due to existing subscription.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResourceNotFound,
            "description": "User or Fund Not Found.",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ValidationErrorResponse,
            "description": "Validation Error.",
        },
    },
)
def subscribe(user_id: str, fund_id: str, amount: float):
    """
    **Subscribe to a Fund**

    Allows a user to subscribe to a specific fund by providing their ID,
    the fund's ID, and the subscription amount.

    **Args**:
    - **user_id** (*str*): The user's unique identifier.
    - **fund_id** (*str*): The fund's unique identifier.
    - **amount** (*float*): The amount to subscribe.

    **Returns**:
    - **dict**: A success or failure message for the subscription.
    """
    service: UserService = UserService(db=db)
    result: ResponseSuccess | ResponseFailure = service.subscribe_to_fund(
        user_id=user_id, fund_id=fund_id, amount=amount
    )
    return JSONResponse(
        content=jsonable_encoder(result), status_code=result.status_code
    )


@app.post(
    path="/cancel/{user_id}/{fund_id}",
    response_model=CancellationSuccessResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": NoActiveSubscriptionErrorResponse,
            "description": "Bad Request due to no active subscription.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResourceNotFound,
            "description": "User or Fund Not Found.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResourceNotFound,
            "description": "Internal Server Error.",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ValidationErrorResponse,
            "description": "Validation Error.",
        },
    },
)
def cancel(user_id: str, fund_id: str):
    """
    **Cancel Subscription**

    Cancels a user's active subscription to a specific fund.

    **Args**:
    - **user_id** (*str*): The user's unique identifier.
    - **fund_id** (*str*): The fund's unique identifier.

    **Returns**:
    - **dict**: A message indicating the success or failure of the cancellation.
    """
    service: UserService = UserService(db=db)
    result: ResponseSuccess | ResponseFailure = service.cancel_subscription(
        user_id=user_id, fund_id=fund_id
    )
    return JSONResponse(
        content=jsonable_encoder(result), status_code=result.status_code
    )


@app.get(
    path="/history/{user_id}",
    response_model=TransactionHistorySuccessResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": Union[ErrorResourceNotFound, NoTransactionsFoundErrorResponse],
            "description": "User Not Found or No Transactions Found.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResourceNotFound,
            "description": "Internal Server Error.",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ValidationErrorResponse,
            "description": "Validation Error.",
        },
    },
)
def history(user_id: str):
    """
    **Get Transaction History**

    Retrieves the transaction history for a specific user.

    **Args**:
    - **user_id** (*str*): The user's unique identifier.

    **Returns**:
    - **dict**: The user's transaction history.
    """
    service: UserService = UserService(db=db)
    result: ResponseSuccess | ResponseFailure = service.get_transaction_history(
        user_id=user_id
    )

    return JSONResponse(
        content=jsonable_encoder(result), status_code=result.status_code
    )
