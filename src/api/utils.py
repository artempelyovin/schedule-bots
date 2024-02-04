from typing import Any, Generic, Iterable, Type, TypeVar

from pydantic import BaseModel, Field
from starlette.status import HTTP_200_OK

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class _BaseResponse(BaseModel, Generic[PydanticModel]):
    status_code: int = Field(default=HTTP_200_OK, description="HTTP статус код")
    error: bool = Field(
        default=False,
        description="Наличие ошибки (`true`, если присутствует ошибка и `false` в противном случае)",
    )
    detail: str | None = Field(
        default=None,
        description='Детальное описание ошибки. `null`, если отсутствует ошибка (`"error": false`)',
    )


class Response(_BaseResponse[PydanticModel]):
    data: PydanticModel | None = None


def write_response(
    serializer: Type[PydanticModel],
    content: Any,
    status_code: int = HTTP_200_OK,
    error: bool = False,
    detail: str | None = None,
) -> Response[PydanticModel]:
    return Response[serializer].model_validate(  # type: ignore
        {
            "data": content,
            "status_code": status_code,
            "error": error,
            "detail": detail,
        }
    )


class ResponseList(_BaseResponse[PydanticModel]):
    data: list[PydanticModel]


def write_response_list(  # TODO: объединить в будущем в `write_response`, сделав нормальный function-generic
    serializer: Type[PydanticModel],
    content: Iterable[Any],
    status_code: int = HTTP_200_OK,
    error: bool = False,
    detail: str | None = None,
) -> ResponseList[PydanticModel]:
    return ResponseList[serializer].model_validate(  # type: ignore
        {
            "data": content,
            "status_code": status_code,
            "error": error,
            "detail": detail,
        }
    )
