from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from src.api.schemas import UniversityShortScheme, UniversityDetailScheme
from src.api.utils import Response, ResponseList, write_response, write_response_list
from src.managers.university import UniversityManager

router = APIRouter(tags=[""])


@router.get("/api/v1/universities")
async def get_universities() -> ResponseList[UniversityShortScheme]:
    universities = await UniversityManager.get_all()
    return write_response_list(serializer=UniversityShortScheme, content=universities)


@router.get("/api/v1/universities/{university_id}")
async def get_university(university_id: int) -> Response[UniversityDetailScheme]:
    university = await UniversityManager.get_by_id(university_id)
    if not university:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Университет с ID={university_id} не найден",
        )
    return write_response(serializer=UniversityDetailScheme, content=university)
