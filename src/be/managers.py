from collections.abc import Sequence
from datetime import date, time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from be.db import Session
from be.db.models import DayOfWeek
from src.be.db.models import Group, Institute, Lesson, University


class UniversityManager:
    @staticmethod
    async def add(session: AsyncSession, name: str) -> University:
        university = University(name=name)
        session.add(university)
        await session.flush()
        return university

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
    async def add(session: AsyncSession, name: str, university_id: int) -> Institute:
        institute = Institute(name=name, university_id=university_id)
        session.add(institute)
        await session.flush()
        return institute

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

    @staticmethod
    async def get_by_name(session: AsyncSession, name: str) -> Institute | None:
        query = select(Institute).where(Institute.name == name)
        return (await session.execute(query)).unique().scalar_one_or_none()


class GroupManager:
    @staticmethod
    async def add(session: AsyncSession, name: str, course: int, is_magistracy: bool, institute_id: int) -> Group:
        institute = Group(name=name, course=course, is_magistracy=is_magistracy, institute_id=institute_id)
        session.add(institute)
        await session.flush()
        return institute

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

    @staticmethod
    async def get_by_name(session: AsyncSession, name: str) -> Group | None:
        query = select(Group).where(Group.name == name)
        return (await session.execute(query)).unique().scalar_one_or_none()


class LessonManager:
    @staticmethod
    async def add(
        session: AsyncSession,
        is_numerator: bool,
        day: DayOfWeek,
        start_time: time,
        end_time: time,
        content: list[str],
        group_id: int,
        valid_from: date,
        valid_to: date,
    ) -> Lesson:
        lesson = Lesson(
            is_numerator=is_numerator,
            day=day,
            start_time=start_time,
            end_time=end_time,
            content=content,
            group_id=group_id,
            valid_from=valid_from,
            valid_to=valid_to,
        )
        session.add(lesson)
        await session.flush()
        return lesson

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
