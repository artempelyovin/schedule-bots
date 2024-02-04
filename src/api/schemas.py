from datetime import time
from enum import IntEnum

from pydantic import BaseModel, ConfigDict, Field


class Course(IntEnum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5


class DayOfWeek(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class _OrmBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LessonDetailedScheme(_OrmBaseModel):
    id: int = Field(description="ID строки занятия")
    day: DayOfWeek = Field(
        description="День недели, к рамках которого предоставлено занятие", examples=[DayOfWeek.TUESDAY]
    )
    start_time: time = Field(description="Время начала занятия (формат: `ЧЧ:ММ:СС`)", examples=[time(8, 30, 00)])
    end_time: time = Field(description="Время окончания занятия (формат: `ЧЧ:ММ:СС`)", examples=[time(10, 00, 00)])
    content: str = Field(
        description="Описание занятия",
        examples=[
            "Численные методы параллельной обработки данных лк 420-3 Лексин А.Ю.",
            "Вариационное исчисление лб 106-3 Прохоров А.В.",
        ],
    )


class GroupShortScheme(_OrmBaseModel):
    id: int = Field(description="ID группы")
    short_name: str = Field(description="Аббревиатура группы", examples=["ПМИ"])


class GroupDetailScheme(GroupShortScheme):
    full_name: str = Field(
        description="Расшифровка аббревиатуры группы",
        examples=["Прикладная математика и информатика"],
    )
    description: str = Field(
        description="Короткое описание группы",
        examples=["Подготовка компетентных специалистов в области разработки программного обеспечения"],
    )
    course: Course = Field(description="Курс", examples=[Course.FIRST])
    is_master_program: bool = Field(description="Является ли группа магистратурой?", examples=[False])


class InstituteShortScheme(_OrmBaseModel):
    id: int = Field(description="ID института")
    short_name: str = Field(description="Аббревиатура института", examples=["ИИТиЭ"])


class InstituteDetailScheme(InstituteShortScheme):
    full_name: str = Field(
        description="Расшифровка аббревиатуры института",
        examples=["Институт информационных технологий и электроники"],
    )
    description: str = Field(
        description="Короткое описание института",
        examples=["Институт, созданный объединений двух других: ИПМФиИ и ИИТР"],
    )
    groups: list[GroupShortScheme] = Field(description="Список групп, прикреплённых к данному институту")


class UniversityShortScheme(_OrmBaseModel):
    id: int = Field(description="ID университета")
    short_name: str = Field(description="Аббревиатура университета", examples=["ВлГУ"])


class UniversityDetailScheme(UniversityShortScheme):
    full_name: str = Field(
        description="Расшифровка аббревиатуры университета",
        examples=[
            "Владимирский государственный университет имени Александра Григорьевича и Николая Григорьевича Столетовых"
        ],
    )
    description: str = Field(
        description="Короткое описание института",
        examples=["Один из ведущих вузов ЦФО, центр инновационного, технологического и социального развития региона."],
    )
    institutes: list[InstituteShortScheme] = Field(
        description="Список институтов, прикреплённых к данному университету"
    )
