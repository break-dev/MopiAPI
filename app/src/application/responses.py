from pydantic.generics import GenericModel
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, Union, List, Dict, Any
from fastapi.responses import FileResponse

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
    title: str
    extension: str
    file: FileResponse


class RES_GetIframe(BaseModel):
    url: str
