from datetime import time
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Course(StrEnum):
    FIRST = "FIRST"
    SECOND = "SECOND"
    THIRD = "THIRD"
    FOURTH = "FOURTH"
    FIFTH = "FIFTH"


class DayOfWeek(StrEnum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


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
    institutes: list[InstituteShortScheme] = Field(
        description="Список институтов, прикреплённых к данному университету"
    )
