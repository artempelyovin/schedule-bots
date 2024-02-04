from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND

from src.be.api.utils import Response


class UniversityNotFoundException(HTTPException):
    def __init__(self, university_id: int) -> None:
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=f"Университет с ID={university_id} не найден")


class InstituteNotFoundException(HTTPException):
    def __init__(self, institute_id: int) -> None:
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=f"Институт с ID={institute_id} не найден")


class GroupNotFoundException(HTTPException):
    def __init__(self, group_id: int) -> None:
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=f"Группа с ID={group_id} не найдена")


async def http_exception_handler(
    request: Request,  # noqa: ARG001
    exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=Response(data=None, status_code=exc.status_code, error=True, detail=exc.detail).model_dump(),
    )
