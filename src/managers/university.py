from typing import Sequence

from sqlalchemy import select

from src.db.core import Session
from src.db.models.university import University


class UniversityManager:
    @staticmethod
    async def get_all() -> Sequence[University]:
        async with Session() as session:
            query = select(University)
            univ_stmt = await session.execute(query)
            return univ_stmt.scalars().all()

    @staticmethod
    async def get_by_id(university_id: int) -> University | None:
        async with Session() as session:
            query = select(University).where(University.id == university_id)
            universities = await session.execute(query)
            return universities.scalar_one_or_none()
