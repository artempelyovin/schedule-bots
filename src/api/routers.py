from fastapi import APIRouter

from src.api.exceptions import GroupNotFoundException, InstituteNotFoundException, UniversityNotFoundException
from src.api.schemas import (
    DayOfWeek,
    GroupDetailScheme,
    InstituteDetailScheme,
    LessonDetailedScheme,
    UniversityDetailScheme,
    UniversityShortScheme,
)
from src.api.utils import Response, ResponseList, write_response, write_response_list
from src.managers import GroupManager, InstituteManager, LessonManager, UniversityManager

router = APIRouter(tags=[""])


@router.get("/api/v1/universities")
async def get_universities() -> ResponseList[UniversityShortScheme]:
    universities = await UniversityManager.get_all()
    return write_response_list(serializer=UniversityShortScheme, content=universities)


@router.get("/api/v1/universities/{university_id}")
async def get_university(university_id: int) -> Response[UniversityDetailScheme]:
    university = await UniversityManager.get_by_id(university_id)
    if not university:
        raise UniversityNotFoundException(university_id)
    return write_response(serializer=UniversityDetailScheme, content=university)


@router.get("/api/v1/institutes/{institute_id}")
async def get_institute(institute_id: int) -> Response[InstituteDetailScheme]:
    institute = await InstituteManager.get_by_id(institute_id)
    if not institute:
        raise InstituteNotFoundException(institute_id)
    return write_response(serializer=InstituteDetailScheme, content=institute)


@router.get("/api/v1/groups/{group_id}")
async def get_group(group_id: int) -> Response[GroupDetailScheme]:
    group = await GroupManager.get_by_id(group_id)
    if not group:
        raise GroupNotFoundException(group_id)
    return write_response(serializer=GroupDetailScheme, content=group)


@router.get("/api/v1/groups/{group_id}/lessons")
async def get_group_lessons(group_id: int) -> ResponseList[LessonDetailedScheme]:
    lessons = await LessonManager.get_lessons_by_group(group_id)
    return write_response_list(serializer=LessonDetailedScheme, content=lessons)


@router.get("/api/v1/groups/{group_id}/days/{day}/lessons")
async def get_group_lessons_by_day(group_id: int, day: DayOfWeek) -> ResponseList[LessonDetailedScheme]:
    lessons = await LessonManager.get_lessons_by_group_and_day(group_id, day)
    return write_response_list(serializer=LessonDetailedScheme, content=lessons)
