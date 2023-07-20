import logging
import sys
from typing import Union

from fastapi import Request
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse, Response

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.getLevelName(logging.DEBUG))


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    query_params = request.query_params._dict
    detail = {"errors": exc.errors(), "query_params": query_params}
    logger.error(detail)
    return await _request_validation_exception_handler(request, exc)


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> Union[JSONResponse, Response]:
    detail = {"errors": exc.detail}
    query_params = request.query_params._dict
    logger.error({"detail": detail, "query_params": query_params})
    return await _http_exception_handler(request, exc)


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> PlainTextResponse:
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.error(
        f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value} >'
    )
    return PlainTextResponse(str(exc), status_code=500)
