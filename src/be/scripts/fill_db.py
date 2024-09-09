import argparse
import asyncio
import json
import logging
from datetime import datetime, time
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from be.db import Session
from be.db.models import DayOfWeek
from be.managers import GroupManager, InstituteManager, LessonManager, UniversityManager

parser = argparse.ArgumentParser(description="Скрипт заполнения базы данных из JSON файла с расписанием")
parser.add_argument("--from", type=str, required=True, help="Путь до JSON файла с расписанием")
parser.add_argument(
    "--valid-from", type=str, required=True, help="Дата в формате YYYY-MM-DD, с которой данное расписание действительно"
)
parser.add_argument(
    "--valid-to", type=str, required=True, help="Дата YYYY-MM-DD, до которой данное расписание действительно"
)
args = parser.parse_args()

logger = logging.getLogger(__name__)


class PairSchedule(BaseModel):  # Расписание КОНКРЕТНОЙ пары
    number: Literal[1, 2, 3, 4, 5, 6, 7]
    start_time: time
    end_time: time
    lessons: list[str]


class DailySchedule(BaseModel):  # Расписание КОНКРЕТНОГО дня
    day: DayOfWeek
    numerator: list[PairSchedule] | None
    denominator: list[PairSchedule] | None


class GroupSchedule(BaseModel):  # Расписание КОНКРЕТНОЙ группы
    university: str
    institute: str
    group: str
    is_magistracy: bool
    course: Literal[1, 2, 3, 4, 5, 6]
    schedule: list[DailySchedule]


def load_schedule(filepath: str) -> list[GroupSchedule]:
    with Path(filepath).open(encoding="utf-8") as file:
        return [GroupSchedule(**group_schedule) for group_schedule in json.load(file)]


async def main() -> None:
    filepath = getattr(args, "from")
    try:
        valid_from = datetime.strptime(args.valid_from, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Параметр --valid-from должен быть в формате YYYY-MM-DD") from None
    try:
        valid_to = datetime.strptime(args.valid_to, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Параметр --valid-to должен быть в формате YYYY-MM-DD") from None

    schedule = load_schedule(filepath=filepath)

    session = Session()
    try:
        # Университет пока тупо захардкожен
        university = await UniversityManager.add(session=session, name="ВлГУ")
        for group_info in schedule:
            institute = await InstituteManager.get_by_name(session=session, name=group_info.institute)
            if not institute:
                institute = await InstituteManager.add(
                    session=session, name=group_info.institute, university_id=university.id
                )
            group = await GroupManager.add(
                session=session,
                name=group_info.group,
                course=group_info.course,
                is_magistracy=group_info.is_magistracy,
                institute_id=institute.id,
            )

            for daily_schedule in group_info.schedule:
                if daily_schedule.numerator:
                    for lesson in daily_schedule.numerator:
                        await LessonManager.add(
                            session=session,
                            is_numerator=True,
                            lesson_number=lesson.number,
                            day=daily_schedule.day,
                            start_time=lesson.start_time,
                            end_time=lesson.end_time,
                            content=lesson.lessons,
                            group_id=group.id,
                            valid_from=valid_from,
                            valid_to=valid_to,
                        )
                if daily_schedule.denominator:
                    for lesson in daily_schedule.denominator:
                        await LessonManager.add(
                            session=session,
                            is_numerator=False,
                            lesson_number=lesson.number,
                            day=daily_schedule.day,
                            start_time=lesson.start_time,
                            end_time=lesson.end_time,
                            content=lesson.lessons,
                            group_id=group.id,
                            valid_from=valid_from,
                            valid_to=valid_to,
                        )
        await session.commit()
    except Exception:
        logger.exception("Database error:")
        await session.rollback()
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
