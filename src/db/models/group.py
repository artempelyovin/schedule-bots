from enum import IntEnum

from sqlalchemy import String, Text, Enum, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import Base


class Course(IntEnum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_name: Mapped[str] = mapped_column(String(8), index=True)  # TODO: оптимально ли 8 символов?
    # TODO: аналогично понять длину для `full_name
    full_name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    course: Mapped[Course] = mapped_column(Enum(Course))
    is_master_program: Mapped[bool] = mapped_column(Boolean, server_default="0")

    institute_id: Mapped[int] = mapped_column(ForeignKey("institute.id"))
