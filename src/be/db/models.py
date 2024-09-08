from datetime import date, datetime, time
from enum import StrEnum
from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class DayOfWeek(StrEnum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class MessengerType(StrEnum):
    VK = "VK"
    TELEGRAM = "TELEGRAM"


VK = MessengerType.VK
TELEGRAM = MessengerType.TELEGRAM


class UserState(StrEnum):
    UNKNOWN = "unknown"
    START = "start"
    ABOUT_BOT = "about_bot"
    ERROR_REPORT = "error_report"
    CHOICE_UNIVERSITY = "choice_university"
    CHOICE_INSTITUTE = "choice_institute"
    CHOICE_COURSE = "choice_course"
    CHOICE_GROUP = "choice_group"
    DISPLAY_SCHEDULE = "display_schedule"


class Lesson(Base, TimestampMixin):
    __tablename__ = "lesson"

    __table_args__ = (
        UniqueConstraint(
            "is_numerator",
            "day",
            "start_time",
            "end_time",
            "valid_from",
            "valid_to",
            "group_id",
            name="unique_lesson_for_group",
        ),
        CheckConstraint("start_time < end_time"),
        CheckConstraint("valid_from < valid_to"),
        CheckConstraint("lesson_number >= 1 AND lesson_number <= 7"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    is_numerator: Mapped[bool] = mapped_column(Boolean, server_default="0")
    day: Mapped[DayOfWeek] = mapped_column(Enum(DayOfWeek, name="day"))
    lesson_number: Mapped[int] = mapped_column(SmallInteger)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    content: Mapped[list[str] | None] = mapped_column(JSON)  # TODO: со временем более "правильное" название
    valid_from: Mapped[date] = mapped_column(Date)
    valid_to: Mapped[date] = mapped_column(Date)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))


class Group(Base, TimestampMixin):
    __tablename__ = "group"
    __table_args__ = (CheckConstraint("course >= 1 AND course <= 6"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    course: Mapped[int] = mapped_column(Integer)
    is_magistracy: Mapped[bool] = mapped_column(Boolean, server_default="false")
    institute_id: Mapped[int] = mapped_column(ForeignKey("institute.id"))


class Institute(Base, TimestampMixin):
    __tablename__ = "institute"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    university_id: Mapped[int] = mapped_column(ForeignKey("university.id"))

    groups: Mapped[list[Group]] = relationship(lazy="joined")


class University(Base, TimestampMixin):
    __tablename__ = "university"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    institutes: Mapped[list[Institute]] = relationship(lazy="joined")


class User(Base, TimestampMixin):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("user_id", "messenger", name="unique_user_in_messenger"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    state: Mapped[UserState] = mapped_column(Enum(UserState, name="user_state"))
    payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    messenger: Mapped[MessengerType] = mapped_column(Enum(MessengerType, name="messenger"))

    def __str__(self) -> str:
        return (
            f"User("
            f"user_id={self.user_id}, "
            f"username={self.username}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"state={self.state}, "
            f"payload={self.payload}, "
            f"messenger={self.messenger}"
            f")"
        )
