from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

#
from core.logger import logger
from shared._response import error_response, ApiResponse


def filter_exception(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning("Error HTTP: %s %s", f"{request.url} - {exc.detail}", exc)
        return JSONResponse(content=error_response().model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        errores = [
            f"{'.'.join(str(x) for x in err.get('loc', []))}: {err.get('msg')}"
            for err in exc.errors()
        ]
        res = ApiResponse(success=False, error=errores)
        return JSONResponse(content=res.model_dump())

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception("Hubo una excepción: %s", exc)
        return JSONResponse(content=error_response().model_dump())
