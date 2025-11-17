from pydantic.generics import GenericModel
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, Union, List, Dict, Any

T = TypeVar("T")


class Respuesta(GenericModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[Union[str, List[str], Dict[str, Any]]] = None


def errorResponse(error="Ups! Hubo un error"):
    return Respuesta(success=False, error=error)


def validResponse(data):
    return Respuesta(success=True, data=data)


#


class RES_FileResponse(BaseModel):
    folder_name: str
    file_path: str
    file_name: str
    extension: str
    media_type: str


class RES_GetIframe(BaseModel):
    url: str
