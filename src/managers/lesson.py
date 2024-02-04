from typing import Sequence

from sqlalchemy import select

from src.api.schemas import DayOfWeek
from src.db.core import Session
from src.db.models import Lesson


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
                select(Lesson)
                .where((Lesson.group_id == group_id) & (Lesson.day == day))
                .order_by(Lesson.start_time)
            )
            return (await session.execute(query)).unique().scalars().all()
