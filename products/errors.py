from common.errors import BaseHTTPError
from fastapi import status


class ProductNameAlreadyExistsError(BaseHTTPError):
    """
    (400) Product name already exists error
    """

    def __init__(self, *, message="Product name already exists", headers=None):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST, headers=headers)