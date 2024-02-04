from fastapi import APIRouter

from src.api.exceptions import NotFoundException
from src.api.schemas import (
    DayOfWeek,
    GroupDetailScheme,
    InstituteDetailScheme,
    ScheduleDetailedScheme,
    UniversityDetailScheme,
    UniversityShortScheme,
)
from src.api.utils import Response, ResponseList, write_response, write_response_list
from src.managers.group import GroupManager
from src.managers.institute import InstituteManager
from src.managers.schedule import ScheduleManager
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
        raise NotFoundException(f"Университет с ID={university_id} не найден")
    return write_response(serializer=UniversityDetailScheme, content=university)


@router.get("/api/v1/institutes/{institute_id}")
async def get_institute(institute_id: int) -> Response[InstituteDetailScheme]:
    institute = await InstituteManager.get_by_id(institute_id)
    if not institute:
        raise NotFoundException(f"Институт с ID={institute_id} не найден")
    return write_response(serializer=InstituteDetailScheme, content=institute)


@router.get("/api/v1/groups/{group_id}")
async def get_group(group_id: int) -> Response[GroupDetailScheme]:
    group = await GroupManager.get_by_id(group_id)
    if not group:
        raise NotFoundException(f"Группа с ID={group_id} не найдена")
    return write_response(serializer=GroupDetailScheme, content=group)


@router.get("/api/v1/groups/{group_id}/schedules")
async def get_group_schedules(group_id: int) -> ResponseList[ScheduleDetailedScheme]:
    schedules = await ScheduleManager.get_schedules_by_group(group_id)
    return write_response_list(serializer=ScheduleDetailedScheme, content=schedules)


@router.get("/api/v1/groups/{group_id}/days/{day}/schedules")
async def get_group_schedules_by_day(group_id: int, day: DayOfWeek) -> ResponseList[ScheduleDetailedScheme]:
    schedules = await ScheduleManager.get_schedules_by_group_and_day(group_id, day)
    return write_response_list(serializer=ScheduleDetailedScheme, content=schedules)
