from datetime import time

from sqlalchemy import Boolean, Enum, ForeignKey, String, Text, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.be.api.schemas import Course, DayOfWeek


class Base(DeclarativeBase):
    pass


class Lesson(Base):
    __tablename__ = "lesson"

    id: Mapped[int] = mapped_column(primary_key=True)
    day: Mapped[DayOfWeek] = mapped_column(Enum(DayOfWeek, name="day"))
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    content: Mapped[str] = mapped_column(Text)  # TODO: со временем более "правильное" название

    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_name: Mapped[str] = mapped_column(String(8), index=True)  # TODO: оптимально ли 8 символов?
    # TODO: аналогично понять длину для `full_name
    full_name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    course: Mapped[Course] = mapped_column(Enum(Course, name="course"))
    is_master_program: Mapped[bool] = mapped_column(Boolean, server_default="0")

    institute_id: Mapped[int] = mapped_column(ForeignKey("institute.id"))


class Institute(Base):
    __tablename__ = "institute"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_name: Mapped[str] = mapped_column(String(8), index=True)  # TODO: оптимально ли 8 символов?
    # TODO: аналогично понять длину для `full_name`
    full_name: Mapped[str] = mapped_column(String(256), index=True, unique=True)

    university_id: Mapped[int] = mapped_column(ForeignKey("university.id"))
    groups: Mapped[list[Group]] = relationship(lazy="joined")


class University(Base):
    __tablename__ = "university"

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: проанализировать список университетов России и исходя из этого понять максимальную длину для `short_name`
    short_name: Mapped[str] = mapped_column(String(8), index=True)
    # TODO: аналогично понять длину для `full_name`
    full_name: Mapped[str] = mapped_column(String(256), index=True, unique=True)

    institutes: Mapped[list[Institute]] = relationship(lazy="joined")
