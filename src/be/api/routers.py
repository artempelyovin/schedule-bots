from fastapi import APIRouter

from src.be.api.exceptions import GroupNotFoundException, InstituteNotFoundException, UniversityNotFoundException
from src.be.api.schemas import DayOfWeek, GroupScheme, InstituteScheme, LessonScheme, UniversityScheme
from src.be.api.utils import Response, ResponseList, write_response, write_response_list
from src.be.managers import GroupManager, InstituteManager, LessonManager, UniversityManager

router = APIRouter(tags=[""])


@router.get("/api/v1/universities")
async def get_universities() -> ResponseList[UniversityScheme]:
    universities = await UniversityManager.get_all()
    return write_response_list(serializer=UniversityScheme, content=universities)


@router.get("/api/v1/universities/{university_id}")
async def get_university(university_id: int) -> Response[UniversityScheme]:
    university = await UniversityManager.get_by_id(university_id)
    if not university:
        raise UniversityNotFoundException(university_id)
    return write_response(serializer=UniversityScheme, content=university)


@router.get("/api/v1/universities/{university_id}/institutes")
async def get_institutes(university_id: int) -> ResponseList[InstituteScheme]:
    institutes = await InstituteManager.get_by_university(university_id)
    return write_response_list(serializer=InstituteScheme, content=institutes)


@router.get("/api/v1/institutes/{institute_id}")
async def get_institute(institute_id: int) -> Response[InstituteScheme]:
    institute = await InstituteManager.get_by_id(institute_id)
    if not institute:
        raise InstituteNotFoundException(institute_id)
    return write_response(serializer=InstituteScheme, content=institute)


@router.get("/api/v1/institutes/{institute_id}/groups")
async def get_groups(institute_id: int) -> ResponseList[GroupScheme]:
    groups = await GroupManager.get_by_institute(institute_id)
    return write_response_list(serializer=GroupScheme, content=groups)


@router.get("/api/v1/groups/{group_id}")
async def get_group(group_id: int) -> Response[GroupScheme]:
    group = await GroupManager.get_by_id(group_id)
    if not group:
        raise GroupNotFoundException(group_id)
    return write_response(serializer=GroupScheme, content=group)


@router.get("/api/v1/groups/{group_id}/lessons")
async def get_group_lessons(group_id: int) -> ResponseList[LessonScheme]:
    lessons = await LessonManager.get_lessons_by_group(group_id)
    return write_response_list(serializer=LessonScheme, content=lessons)


@router.get("/api/v1/groups/{group_id}/days/{day}/lessons")
async def get_group_lessons_by_day(group_id: int, day: DayOfWeek) -> ResponseList[LessonScheme]:
    lessons = await LessonManager.get_lessons_by_group_and_day(group_id, day)
    return write_response_list(serializer=LessonScheme, content=lessons)
