from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base
from src.db.models.group import Group


class Institute(Base):
    __tablename__ = "institute"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_name: Mapped[str] = mapped_column(String(8), index=True)  # TODO: оптимально ли 8 символов?
    # TODO: аналогично понять длину для `full_name`
    full_name: Mapped[str] = mapped_column(String(256), index=True, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    university_id: Mapped[int] = mapped_column(ForeignKey("university.id"))
    groups: Mapped[list["Group"]] = relationship(lazy="joined")
