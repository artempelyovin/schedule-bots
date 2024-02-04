from collections.abc import Sequence

from sqlalchemy import select

from src.be.api.schemas import DayOfWeek
from src.be.db.core import Session
from src.be.db.models import Group, Institute, Lesson, University


class UniversityManager:
    @staticmethod
    async def get_all() -> Sequence[University]:
        async with Session() as session:
            query = select(University)
            return (await session.execute(query)).unique().scalars().all()

    @staticmethod
    async def get_by_id(university_id: int) -> University | None:
        async with Session() as session:
            query = select(University).where(University.id == university_id)
            return (await session.execute(query)).unique().scalar_one_or_none()


class InstituteManager:
    @staticmethod
    async def get_by_university(university_id: int) -> Sequence[Institute]:
        async with Session() as session:
            query = select(Institute).where(Institute.university_id == university_id)
            return (await session.execute(query)).unique().scalars().all()

    @staticmethod
    async def get_by_id(institute_id: int) -> Institute | None:
        async with Session() as session:
            query = select(Institute).where(Institute.id == institute_id)
            return (await session.execute(query)).unique().scalar_one_or_none()


class GroupManager:
    @staticmethod
    async def get_by_institute(institute_id: int) -> Sequence[Group]:
        async with Session() as session:
            query = select(Group).where(Group.institute_id == institute_id)
            return (await session.execute(query)).unique().scalars().all()

    @staticmethod
    async def get_by_id(group_id: int) -> Group | None:
        async with Session() as session:
            query = select(Group).where(Group.id == group_id)
            return (await session.execute(query)).unique().scalar_one_or_none()


class LessonManager:
    @staticmethod
    async def get_lessons_by_group(group_id: int) -> Sequence[Lesson]:
        async with Session() as session:
            query = select(Lesson).where(Lesson.group_id == group_id).order_by(Lesson.day, Lesson.start_time)
            return (await session.execute(query)).unique().scalars().all()

    @staticmethod
    async def get_lessons_by_group_and_day(group_id: int, day: DayOfWeek) -> Sequence[Lesson]:
        async with Session() as session:
            query = (
                select(Lesson).where((Lesson.group_id == group_id) & (Lesson.day == day)).order_by(Lesson.start_time)
            )
            return (await session.execute(query)).unique().scalars().all()
