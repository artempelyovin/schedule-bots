from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base
from src.db.models.institute import Institute


class University(Base):
    __tablename__ = "university"

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: проанализировать список университетов России и исходя из этого понять максимальную длину для `short_name`
    short_name: Mapped[str] = mapped_column(String(8), index=True)
    # TODO: аналогично понять длину для `full_name`
    full_name: Mapped[str] = mapped_column(String(256), index=True, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    institutes: Mapped[list["Institute"]] = relationship(lazy="joined")
