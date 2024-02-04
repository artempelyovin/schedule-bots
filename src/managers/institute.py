from sqlalchemy import select

from src.db.core import Session
from src.db.models import Institute


class InstituteManager:
    @staticmethod
    async def get_by_id(university_id: int) -> Institute | None:
        async with Session() as session:
            query = select(Institute).where(Institute.id == university_id)
            return (await session.execute(query)).unique().scalar_one_or_none()
