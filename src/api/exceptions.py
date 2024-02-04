from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND

from src.api.utils import Response


class NotFoundException(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=Response(data=None, status_code=exc.status_code, error=True, detail=exc.detail).model_dump(),
    )
