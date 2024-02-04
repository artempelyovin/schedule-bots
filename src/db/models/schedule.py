from datetime import time
from enum import IntEnum

from sqlalchemy import Text, ForeignKey, Time, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import Base


class DayOfWeek(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    day: Mapped[DayOfWeek] = mapped_column(Enum(DayOfWeek))
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    content: Mapped[str] = mapped_column(Text)  # TODO: со временем более "правильное" название

    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
