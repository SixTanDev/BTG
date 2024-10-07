"""
Unit tests for ResponseFailure and ResponseSuccess classes.

This module contains tests to verify the initialization, behavior, and
status code mappings for the `ResponseFailure` and `ResponseSuccess`
response classes in various scenarios.
"""

from starlette import status
from btg.response import ResponseTypes, ResponseFailure, ResponseSuccess


def test_response_failure_initialization():
    """
    Test for initializing `ResponseFailure` with a message.

    This test checks that the `ResponseFailure` is correctly
    initialized with the provided error type and message, and
    that the status code is mapped correctly based on the type.
    """
    # Arrange
    error_type = ResponseTypes.RESOURCE_ERROR
    message = "Resource not found"

    # Act
    response_failure = ResponseFailure(type_=error_type, message=message)

    # Assert
    assert response_failure.type == error_type
    assert response_failure.status_code == status.HTTP_404_NOT_FOUND
    assert response_failure.message == message
    assert not response_failure  # ResponseFailure should evaluate to False


def test_response_failure_with_exception():
    """
    Test for initializing `ResponseFailure` with an Exception.

    This test checks that when an Exception is passed as the message, the error message
    is formatted correctly to include the exception class name.
    """
    # Arrange
    error_type = ResponseTypes.SYSTEM_ERROR
    exception = ValueError("Invalid value")

    # Act
    response_failure = ResponseFailure(type_=error_type, message=exception)

    # Assert
    assert response_failure.type == error_type
    assert response_failure.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response_failure.message == "ValueError: Invalid value"
    assert not response_failure  # ResponseFailure should evaluate to False


def test_response_failure_default_status_code():
    """
    Test for `ResponseFailure` using an unknown error type.

    This test checks that if an unknown error type is provided, the default status code
    is set to 400 (Bad Request).
    """
    # Arrange
    unknown_error_type = "UnknownError"
    message = "Unknown error occurred"

    # Act
    response_failure = ResponseFailure(type_=unknown_error_type, message=message)

    # Assert
    assert response_failure.type == unknown_error_type
    assert response_failure.status_code == status.HTTP_400_BAD_REQUEST
    assert response_failure.message == message
    assert not response_failure  # ResponseFailure should evaluate to False


def test_response_failure_value():
    """
    Test for the `value` property of `ResponseFailure`.

    This test checks that the `value` property returns a dictionary containing the type,
    message, and status_code of the failure.
    """
    # Arrange
    error_type = ResponseTypes.CONFLICT_ERROR
    message = "Resource conflict"

    # Act
    response_failure = ResponseFailure(type_=error_type, message=message)
    response_value = response_failure.value

    # Assert
    assert response_value == {
        "type": error_type,
        "message": message,
        "status_code": status.HTTP_409_CONFLICT,
    }


def test_response_success_initialization():
    """
    Test for initializing `ResponseSuccess`.

    This test checks that the `ResponseSuccess` is correctly initialized with
    the provided response type and value, and that the status code is correctly
    mapped.
    """
    # Arrange
    response_type = ResponseTypes.CREATED
    value = {"id": 123, "name": "New resource"}

    # Act
    response_success = ResponseSuccess(response_type=response_type, value=value)

    # Assert
    assert response_success.type == response_type
    assert response_success.status_code == status.HTTP_201_CREATED
    assert response_success.value == value
    assert response_success  # ResponseSuccess should evaluate to True


def test_response_success_default_type():
    """
    Test for default initialization of `ResponseSuccess`.

    This test checks that when no response type is provided, the default type is set to
    `ResponseTypes.SUCCESS` and the status code is 200 (OK).
    """
    # Act
    response_success = ResponseSuccess()

    # Assert
    assert response_success.type == ResponseTypes.SUCCESS
    assert response_success.status_code == status.HTTP_200_OK
    assert response_success.value is None
    assert response_success  # ResponseSuccess should evaluate to True
