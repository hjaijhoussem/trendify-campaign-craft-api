from typing import Dict

from fastapi import status


class SvBoilError(Exception):
    pass


class BaseHTTPError(SvBoilError):
    """
    A base class for HTTP errors.

    Attributes:
        message (str): The error message.
        status_code (int): The HTTP status code associated with the error.
        headers (dict): The headers to include in the HTTP response.
    """

    def __init__(self, message: str, status_code: int = 500, headers: dict = None):
        """
        Initializes a new instance of the BaseHTTPException class.

        Args:
            message (str): The error message.
            status_code (int, optional): The HTTP status code associated with the error. Defaults to None.
            headers (dict, optional): The headers to include in the HTTP response. Defaults to None.
        """
        self.message = message
        self.code = status_code
        self.error = self.get_error_code()
        self.headers = headers or {}

        # Convert header values to strings
        for key, value in self.headers.items():
            if isinstance(value, (tuple, list, set)):
                self.headers[key] = ", ".join(str(element) for element in value)
            else:
                self.headers[key] = str(value)

        # Set default X-Error header if not already present
        if "X-Error" not in self.headers:
            self.headers["X-Error"] = self.get_error_code()

        super().__init__(self.message)

    def __str__(self):
        """
        Returns the error message.
        """
        return self.message

    def dict(self) -> Dict[str, any]:
        """
        Returns a dictionary representation of the error.

        Returns:
            dict: A dictionary containing the error message, status code, and headers.
        """
        return {
            # "message": self.message,
            # "headers": self.headers,
            "code": self.code,
            "error": self.error,
        }

    def get_error_code(self) -> str:
        """
        Returns the name of the exception class.

        Returns:
            str: The name of the exception class.
        """
        return self.__class__.__name__

    def get_default_headers(self) -> Dict[str, str]:
        """
        Returns the default headers for the HTTP response.

        Returns:
            dict: A dictionary containing the X-Error header with the value from `get_error_code()`.
        """
        return {"X-Error": self.get_error_code()}


class DeprecatedEndpointError(BaseHTTPError):
    """
    (410) Exception raised when trying to access a deprecated endpoint that is no longer supported.
    """

    def __init__(
        self,
        message="This endpoint is deprecated and no longer available.",
        headers=None,
    ):
        if headers is None:
            headers = {}
        super().__init__(message=message, status_code=status.HTTP_410_GONE, headers=headers)


class InvalidApiVersionError(BaseHTTPError):
    """
    (401)
    """

    def __init__(self, *, message="The requested API version is not supported", headers=None):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST, headers=headers)


class NotFoundError(BaseHTTPError):
    """
    (404)
    """

    def __init__(self, *, message="The requested resource was not found", headers=None):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND, headers=headers)


class InvalidApiKeyError(BaseHTTPError):
    """
    (401)
    """

    def __init__(self, *, message="Invalid API key", headers=None):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED, headers=headers)


class MissingRequiredParameterError(BaseHTTPError):
    """
    (400)
    """

    def __init__(self, *, message="Missing required parameter", headers=None):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST, headers=headers)