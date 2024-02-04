from typing import Sequence

from sqlalchemy import select

from src.api.schemas import DayOfWeek
from src.db.core import Session
from src.db.models.schedule import Schedule


class ScheduleManager:
    @staticmethod
    async def get_schedules_by_group(group_id: int) -> Sequence[Schedule]:
        async with Session() as session:
            query = select(Schedule).where(Schedule.group_id == group_id).order_by(Schedule.day, Schedule.start_time)
            return (await session.execute(query)).unique().scalars().all()

    @staticmethod
    async def get_schedules_by_group_and_day(group_id: int, day: DayOfWeek) -> Sequence[Schedule]:
        async with Session() as session:
            query = (
                select(Schedule)
                .where((Schedule.group_id == group_id) & (Schedule.day == day))
                .order_by(Schedule.start_time)
            )
            return (await session.execute(query)).unique().scalars().all()
