from collections.abc import Sequence
from datetime import UTC, date, datetime, time
from typing import Any

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from be.db import Session
from be.db.models import DayOfWeek, MessengerType, User, UserState
from src.be.db.models import Group, Institute, Lesson, University


class UniversityManager:
    @staticmethod
    async def add(session: AsyncSession, name: str) -> University:
        university = University(name=name)
        session.add(university)
        await session.flush()
        return university

    @staticmethod
    async def get_all() -> list[University]:
        async with Session() as session:
            query = select(University).order_by(University.name)
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
    async def get_by_university(university_id: int) -> list[Institute]:
        async with Session() as session:
            query = select(Institute).where(Institute.university_id == university_id).order_by(Institute.name)
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
    async def get_courses_info_by_institute(institute_id: int) -> list[tuple[int, bool]]:
        async with Session() as session:
            query = (
                select(Group.course, Group.is_magistracy)
                .where(Group.institute_id == institute_id)
                .group_by(Group.course, Group.is_magistracy)
                .order_by(Group.is_magistracy.asc(), Group.course.asc())
            )

            return (await session.execute(query)).all()

    @staticmethod
    async def get_by_institute_and_course(institute_id: int, course: int, is_magistracy: bool) -> list[Group]:
        async with Session() as session:
            query = (
                select(Group)
                .where(Group.institute_id == institute_id)
                .where(Group.course == course)
                .where(Group.is_magistracy == is_magistracy)
                .order_by(Group.name)
            )
            return (await session.execute(query)).scalars().all()

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
    async def add(  # noqa: PLR0913
        session: AsyncSession,
        is_numerator: bool,
        day: DayOfWeek,
        lesson_number: int,
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
            lesson_number=lesson_number,
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
    async def get_lessons(group_id: int, day: DayOfWeek, is_numerator: bool) -> list[Lesson]:
        today = datetime.now(tz=UTC).date()
        async with Session() as session:
            query = (
                select(Lesson)
                .where(Lesson.group_id == group_id)
                .where(Lesson.day == day)
                .where(Lesson.is_numerator == is_numerator)
                .where(Lesson.valid_from <= today)
                .where(Lesson.valid_to >= today)
                .order_by(Lesson.start_time)
            )
            return (await session.execute(query)).scalars().all()


class UserManager:
    @staticmethod
    async def add(  # noqa: PLR0913
        user_id: int,
        username: str | None,
        first_name: str,
        last_name: str,
        messenger: MessengerType,
        state: UserState = UserState.START,
        payload: dict[str, Any] | None = None,
    ) -> User:
        async with Session() as session:
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                messenger=messenger,
                state=state,
                payload=payload,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def exists(user_id: int, messenger: MessengerType) -> bool:
        async with Session() as session:
            query = select(exists(User.id).where(User.user_id == user_id).where(User.messenger == messenger))
            return (await session.execute(query)).scalar()

    @staticmethod
    async def get(user_id: int, messenger: MessengerType) -> User | None:
        async with Session() as session:
            query = select(User).where(User.user_id == user_id).where(User.messenger == messenger)
            return (await session.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update_state_and_payload(
        user_id: int,
        messenger: MessengerType,
        state: UserState,
        current_payload: dict[str, Any] | None,
    ) -> User:
        async with Session() as session:
            query = select(User).where(User.user_id == user_id).where(User.messenger == messenger)
            user = (await session.execute(query)).scalar()
            user.state = state
            user.payload = current_payload
            await session.commit()
            await session.refresh(user)
            return user
