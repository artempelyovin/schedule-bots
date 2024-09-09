from pydantic import BaseModel, validator

from be.db.models import DayOfWeek, UserState


class Payload(BaseModel):
    state: UserState = UserState.START


StartPayload = Payload(state=UserState.START)
AboutBotPayload = Payload(state=UserState.ABOUT_BOT)
ErrorReportPayload = Payload(state=UserState.ERROR_REPORT)


class PaginationPayload(Payload):
    offset: int = 0


class ChoiceUniversityPayload(PaginationPayload):
    offset: int = 0

    @validator("state", always=True)
    def override_state(cls, _) -> str:  # noqa: N805
        return UserState.CHOICE_UNIVERSITY


class ChoiceInstitutePayload(ChoiceUniversityPayload):
    university_id: int
    offset: int = 0

    @validator("state", always=True)
    def override_state(cls, _) -> str:  # noqa: N805
        return UserState.CHOICE_INSTITUTE


class ChoiceCoursePayload(ChoiceInstitutePayload):
    institute_id: int

    @validator("state", always=True)
    def override_state(cls, _) -> str:  # noqa: N805
        return UserState.CHOICE_COURSE


class ChoiceGroupPayload(ChoiceCoursePayload):
    course: int
    is_magistracy: bool

    @validator("state", always=True)
    def override_state(cls, _) -> str:  # noqa: N805
        return UserState.CHOICE_GROUP


class DisplaySchedulePayload(ChoiceGroupPayload):
    group_id: int
    day: DayOfWeek = DayOfWeek.MONDAY
    is_numerator: bool = True

    @validator("state", always=True)
    def override_state(cls, _) -> str:  # noqa: N805
        return UserState.DISPLAY_SCHEDULE
