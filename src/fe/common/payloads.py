from typing import Type

from pydantic import BaseModel, validator

from be.db.models import DayOfWeek, UserState


class Payload(BaseModel):
    state: str = UserState.START

    @classmethod
    def to_map(cls) -> list[tuple[str, Type]]:
        return [(field_name, field.type_) for field_name, field in cls.__fields__.items()]


StartPayload = Payload(state=UserState.START)
AboutBotPayload = Payload(state=UserState.ABOUT_BOT)
ErrorReportPayload = Payload(state=UserState.ERROR_REPORT)


class PaginationPayload(Payload):
    offset: int = 0


class ChoiceUniversityPayload(PaginationPayload):
    offset: int = 0

    @validator("state", always=True)
    def set_state(cls, _) -> str:
        return UserState.CHOICE_UNIVERSITY


class ChoiceInstitutePayload(ChoiceUniversityPayload):
    university_id: int
    offset: int = 0

    @validator("state", always=True)
    def set_state(cls, _) -> str:
        return UserState.CHOICE_INSTITUTE


class ChoiceCoursePayload(ChoiceInstitutePayload):
    institute_id: int

    @validator("state", always=True)
    def set_state(cls, _) -> str:
        return UserState.CHOICE_COURSE


class ChoiceGroupPayload(ChoiceCoursePayload):
    course: int
    is_magistracy: bool

    @validator("state", always=True)
    def set_state(cls, _) -> str:
        return UserState.CHOICE_GROUP


class DisplaySchedulePayload(ChoiceGroupPayload):
    group_id: int
    day: DayOfWeek = DayOfWeek.MONDAY
    is_numerator: bool = True

    @validator("state", always=True)
    def set_state(cls, _) -> str:
        return UserState.DISPLAY_SCHEDULE
