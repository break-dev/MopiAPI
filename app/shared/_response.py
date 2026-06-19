from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: str = ""


def error_response(message: str = "Ups! Hubo un error") -> ApiResponse[T]:
    return ApiResponse(success=False, message=message)


def valid_response(data: T, message: str = "Operación exitosa") -> ApiResponse[T]:
    return ApiResponse(success=True, data=data, message=message)
