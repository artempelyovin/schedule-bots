from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from src.api.university.schemas import UniversityScheme
from src.api.utils import Response, ResponseList, write_response, write_response_list

router = APIRouter(tags=[""])

ALL_UNIVERSITIES = [  # TODO(issue-1): Доставать университеты из базы, а не из кода!
    UniversityScheme(
        id=1,
        name="ВлГУ",
        description="Владимировский государственный институт имени Александра и Николая Григорьевича Столетовых",
    )
]


@router.get("/api/v1/universities")
async def get_universities() -> ResponseList[UniversityScheme]:
    return write_response_list(serializer=UniversityScheme, content=ALL_UNIVERSITIES)


@router.get("/api/v1/universities/{university_id}")
async def get_university(university_id: int) -> Response[UniversityScheme]:
    for university in ALL_UNIVERSITIES:
        if university.id == university_id:
            return write_response(serializer=UniversityScheme, content=university)
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f"Университет с ID={university_id} не найден",
    )
