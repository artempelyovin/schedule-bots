from datetime import date, datetime, time
from enum import StrEnum

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
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
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    is_numerator: Mapped[bool] = mapped_column(Boolean, server_default="0")
    day: Mapped[DayOfWeek] = mapped_column(Enum(DayOfWeek, name="day"))
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    content: Mapped[list[str]] = mapped_column(JSON)  # TODO: со временем более "правильное" название
    valid_from: Mapped[date] = mapped_column(Date)
    valid_to: Mapped[date] = mapped_column(Date)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))


class Group(Base, TimestampMixin):
    __tablename__ = "group"
    __table_args__ = (CheckConstraint(f"course >= 1 AND course <= 6"),)

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
