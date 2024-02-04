from sqlalchemy import select

from src.db.core import Session
from src.db.models.group import Group


class GroupManager:
    @staticmethod
    async def get_by_id(group_id: int) -> Group | None:
        async with Session() as session:
            query = select(Group).where(Group.id == group_id)
            return (await session.execute(query)).unique().scalar_one_or_none()
