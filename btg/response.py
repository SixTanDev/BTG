"""
This module handles the failure and success responses of the API endpoints.

It defines the `ResponseTypes` class for mapping response
types to HTTP status codes, and the `ResponseFailure` and
`ResponseSuccess` classes for encapsulating response details.
"""

# pylint: disable=R0903

from starlette import status


class ResponseTypes:
    """
    Defines different types of responses and maps them to HTTP status codes.
    """

    PARAMETERS_ERROR = "ParametersError"
    RESOURCE_ERROR = "ResourceError"
    CONFLICT_ERROR = "ConflictError"
    SYSTEM_ERROR = "SystemError"
    SUCCESS = "Success"
    CREATED = "Created"

    # Map response types to HTTP status codes
    STATUS_CODES = {
        PARAMETERS_ERROR: status.HTTP_400_BAD_REQUEST,
        RESOURCE_ERROR: status.HTTP_404_NOT_FOUND,
        CONFLICT_ERROR: status.HTTP_409_CONFLICT,
        SYSTEM_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
        SUCCESS: status.HTTP_200_OK,
        CREATED: status.HTTP_201_CREATED,
    }


class ResponseFailure:
    """
    Represents a failed response, encapsulating the error type,
    message, and HTTP status code.
    """

    def __init__(self, type_: str, message: str | Exception) -> None:
        """
        Initializes a ResponseFailure instance with the given type and message.

        Args:
            type_ (str): The type of error.
            message (str or Exception): A message describing the
                                        error or an Exception instance.
        """
        self.type = type_
        self.status_code = ResponseTypes.STATUS_CODES.get(
            type_, status.HTTP_400_BAD_REQUEST
        )
        self.message = self._format_message(msg=message)

    def _format_message(self, msg: str | Exception) -> str:
        """
        Formats the error message.

        If the message is an Exception, it includes the exception class name.

        Args:
            msg (str or Exception): The error message or Exception instance.

        Returns:
            str: The formatted error message.
        """
        if isinstance(msg, Exception):
            return f"{msg.__class__.__name__}: {msg}"
        return msg

    @property
    def value(self) -> dict:
        """
        Provides a dictionary representation of the error.

        Returns:
            dict: A dictionary containing the error type and message.
        """
        return {
            "type": self.type,
            "message": self.message,
            "status_code": self.status_code,
        }

    def __bool__(self) -> bool:
        """
        Indicates that this is a failed response.

        Returns:
            bool: Always returns False.
        """
        return False


class ResponseSuccess:
    """
    Represents a successful response, containing the result value and HTTP status code.
    """

    def __init__(self, response_type: str = ResponseTypes.SUCCESS, value: any = None):
        """
        Initializes a ResponseSuccess instance with an optional result value.

        Args:
            value: The result data to include in the response.
        """
        self.type: str = response_type
        self.status_code = ResponseTypes.STATUS_CODES.get(self.type)
        self.value: any = value

    def __bool__(self) -> bool:
        """
        Indicates that this is a successful response.

        Returns:
            bool: Always returns True.
        """
        return True
