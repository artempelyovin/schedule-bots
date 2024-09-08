from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Generic, TypeVar
from datetime import date

from vkbottle import KeyboardButtonColor

from be.db.models import DayOfWeek, Group, Institute, Lesson, University
from be.utils import is_numerator, is_denominator
from fe.common.constants import (
    ABOUT_BOT_BUTTON_TEXT,
    ABOUT_BOT_MESSAGE,
    BACK_BUTTON_TEXT,
    CHOICE_COURSE_MESSAGE,
    CHOICE_GROUP_MESSAGE,
    CHOICE_INSTITUTE_MESSAGE,
    CHOICE_UNIVERSITY_MESSAGE,
    COURSE_BUTTON_TEXT,
    COURSE_MAGISTRACY_BUTTON_TEXT,
    DENOMINATOR_TEXT,
    ERROR_REPORT_BUTTON_TEXT,
    ERROR_REPORT_MESSAGE,
    FIND_SCHEDULE_BUTTON_TEXT,
    FRIDAY_BUTTON_TEXT,
    FRIDAY_TEXT,
    GROUP_BUTTON_TEXT,
    LESSON_MESSAGE,
    MONDAY_BUTTON_TEXT,
    MONDAY_TEXT,
    NOT_LESSONS_MESSAGE,
    NUMERATOR_TEXT,
    SATURDAY_BUTTON_TEXT,
    SATURDAY_TEXT,
    SCHEDULE_TITLE_MESSAGE,
    SUNDAY_BUTTON_TEXT,
    SUNDAY_TEXT,
    THURSDAY_BUTTON_TEXT,
    THURSDAY_TEXT,
    TUESDAY_BUTTON_TEXT,
    TUESDAY_TEXT,
    UNIVERSITY_BUTTON_TEXT,
    VK_START_MESSAGE,
    WEDNESDAY_BUTTON_TEXT,
    WEDNESDAY_TEXT, NEXT_WEEK_BUTTON, CURRENT_WEEK_BUTTON,
)
from fe.common.keyboards import Button, Keyboard, Row, _generate_pagination_keyboard
from fe.common.payloads import (
    AboutBotPayload,
    ChoiceCoursePayload,
    ChoiceGroupPayload,
    ChoiceInstitutePayload,
    ChoiceUniversityPayload,
    DisplaySchedulePayload,
    ErrorReportPayload,
    PaginationPayload,
    StartPayload,
)

ERROR_REPORT_BUTTON = Button(
    label=ERROR_REPORT_BUTTON_TEXT, payload=ErrorReportPayload, color=KeyboardButtonColor.NEGATIVE
)
BACK_TO_START_BUTTON = Button(label=BACK_BUTTON_TEXT, payload=StartPayload, color=KeyboardButtonColor.PRIMARY)


class Dialog(ABC):
    @property
    @abstractmethod
    def message(self) -> str:
        pass

    @property
    @abstractmethod
    def keyboard(self) -> Keyboard:
        pass


class StartDialog(Dialog):
    @property
    def message(self) -> str:
        return VK_START_MESSAGE

    @property
    def keyboard(self) -> Keyboard:
        return [
            Button(
                label=FIND_SCHEDULE_BUTTON_TEXT,
                payload=ChoiceUniversityPayload(),
                color=KeyboardButtonColor.POSITIVE,
            ),
            Row(),
            Button(label=ABOUT_BOT_BUTTON_TEXT, payload=AboutBotPayload, color=KeyboardButtonColor.PRIMARY),
            Row(),
            ERROR_REPORT_BUTTON,
        ]


class AboutBotDialog(Dialog):
    @property
    def message(self) -> str:
        return ABOUT_BOT_MESSAGE

    @property
    def keyboard(self) -> Keyboard:
        return [BACK_TO_START_BUTTON, Row(), ERROR_REPORT_BUTTON]


class ErrorReportDialog(Dialog):
    @property
    def message(self) -> str:
        return ERROR_REPORT_MESSAGE

    @property
    def keyboard(self) -> Keyboard:
        return [BACK_TO_START_BUTTON]


T = TypeVar("T")


class PaginationDialog(Generic[T], Dialog, ABC):
    def __init__(self, entities: list[T], current_payload: PaginationPayload):
        self._entities = entities
        self._current_payload = current_payload

    @property
    def start(self) -> int:
        offset = self._current_payload.offset
        return offset + 1  # люди считают с единицы, поэтому всегда +1

    @property
    def stop(self) -> int:
        offset = self._current_payload.offset
        return offset + 6 if offset + 6 < len(self._entities) else len(self._entities)

    @property
    def total(self) -> int:
        return len(self._entities)


class ChoiceUniversityDialog(PaginationDialog[University]):
    def __init__(self, universities: list[University], current_payload: ChoiceUniversityPayload) -> None:
        super().__init__(entities=universities, current_payload=current_payload)

    @property
    def message(self) -> str:
        return CHOICE_UNIVERSITY_MESSAGE.format(start=self.start, stop=self.stop, total=self.total)

    @property
    def keyboard(self) -> Keyboard:
        university_buttons = [
            Button(
                label=UNIVERSITY_BUTTON_TEXT.format(university=university.name),
                payload=ChoiceInstitutePayload(university_id=university.id).dict(),
                color=KeyboardButtonColor.PRIMARY,
            )
            for university in self._entities
        ]

        return _generate_pagination_keyboard(
            current_payload=self._current_payload,
            buttons=university_buttons,
            back_button=BACK_TO_START_BUTTON,
            error_report_button=ERROR_REPORT_BUTTON,
        )


class ChoiceInstituteDialog(PaginationDialog[Institute]):
    def __init__(self, institutes: list[Institute], current_payload: ChoiceInstitutePayload) -> None:
        super().__init__(entities=institutes, current_payload=current_payload)

    @property
    def message(self) -> str:
        return CHOICE_INSTITUTE_MESSAGE.format(start=self.start, stop=self.stop, total=self.total)

    @property
    def keyboard(self) -> Keyboard:
        institutes_buttons = [
            Button(
                label=UNIVERSITY_BUTTON_TEXT.format(university=institute.name),
                payload=ChoiceCoursePayload(**self._current_payload.dict(), institute_id=institute.id).dict(),
                color=KeyboardButtonColor.PRIMARY,
            )
            for institute in self._entities
        ]

        back_button = Button(
            label=BACK_BUTTON_TEXT, payload=ChoiceUniversityPayload(), color=KeyboardButtonColor.PRIMARY
        )

        return _generate_pagination_keyboard(
            current_payload=self._current_payload,
            buttons=institutes_buttons,
            back_button=back_button,
            error_report_button=ERROR_REPORT_BUTTON,
        )


class ChoiceCourseDialog(PaginationDialog[list[tuple[int, bool]]]):
    def __init__(self, courses_info: list[tuple[int, bool]], current_payload: ChoiceCoursePayload) -> None:
        super().__init__(entities=courses_info, current_payload=current_payload)

    @property
    def message(self) -> str:
        return CHOICE_COURSE_MESSAGE.format(start=self.start, stop=self.stop, total=self.total)

    @property
    def keyboard(self) -> Keyboard:
        courses_buttons = [
            Button(
                label=COURSE_MAGISTRACY_BUTTON_TEXT.format(course=course)
                if is_magistracy
                else COURSE_BUTTON_TEXT.format(course=course),
                payload=ChoiceGroupPayload(**self._current_payload.dict(), course=course, is_magistracy=is_magistracy),
                color=KeyboardButtonColor.PRIMARY,
            )
            for course, is_magistracy in self._entities
        ]
        back_button = Button(
            label=BACK_BUTTON_TEXT,
            payload=ChoiceInstitutePayload(**self._current_payload.dict()),
            color=KeyboardButtonColor.PRIMARY,
        )
        return _generate_pagination_keyboard(
            current_payload=self._current_payload,
            buttons=courses_buttons,
            back_button=back_button,
            error_report_button=ERROR_REPORT_BUTTON,
        )


class ChoiceGroupDialog(PaginationDialog[Group]):
    def __init__(self, groups: list[Group], current_payload: ChoiceGroupPayload) -> None:
        super().__init__(entities=groups, current_payload=current_payload)

    @property
    def message(self) -> str:
        return CHOICE_GROUP_MESSAGE.format(start=self.start, stop=self.stop, total=self.total)

    @property
    def keyboard(self) -> Keyboard:
        groups_buttons = [
            Button(
                label=GROUP_BUTTON_TEXT.format(group=group.name),
                payload=DisplaySchedulePayload(**self._current_payload.dict(), group_id=group.id).dict(),
                color=KeyboardButtonColor.PRIMARY,
            )
            for group in self._entities
        ]
        back_button = Button(
            label=BACK_BUTTON_TEXT,
            payload=ChoiceCoursePayload(**self._current_payload.dict()),
            color=KeyboardButtonColor.PRIMARY,
        )
        return _generate_pagination_keyboard(
            current_payload=self._current_payload,
            buttons=groups_buttons,
            back_button=back_button,
            error_report_button=ERROR_REPORT_BUTTON,
        )


class DisplayScheduleDialog(Dialog):
    TEXT_BY_DAY_OF_WEEK = {
        DayOfWeek.MONDAY: MONDAY_TEXT,
        DayOfWeek.TUESDAY: TUESDAY_TEXT,
        DayOfWeek.WEDNESDAY: WEDNESDAY_TEXT,
        DayOfWeek.THURSDAY: THURSDAY_TEXT,
        DayOfWeek.FRIDAY: FRIDAY_TEXT,
        DayOfWeek.SATURDAY: SATURDAY_TEXT,
        DayOfWeek.SUNDAY: SUNDAY_TEXT,
    }

    BUTTON_LABEL_BY_DAY_OF_WEEK = {
        DayOfWeek.MONDAY: MONDAY_BUTTON_TEXT,
        DayOfWeek.TUESDAY: TUESDAY_BUTTON_TEXT,
        DayOfWeek.WEDNESDAY: WEDNESDAY_BUTTON_TEXT,
        DayOfWeek.THURSDAY: THURSDAY_BUTTON_TEXT,
        DayOfWeek.FRIDAY: FRIDAY_BUTTON_TEXT,
        DayOfWeek.SATURDAY: SATURDAY_BUTTON_TEXT,
        DayOfWeek.SUNDAY: SUNDAY_BUTTON_TEXT,
    }
    DAY_OF_WEEK_BY_DAY_NUMBER = {
        0: DayOfWeek.MONDAY,
        1: DayOfWeek.TUESDAY,
        2: DayOfWeek.WEDNESDAY,
        3: DayOfWeek.THURSDAY,
        4: DayOfWeek.FRIDAY,
        5: DayOfWeek.SATURDAY,
        6: DayOfWeek.SUNDAY,
    }
    DAY_NUMBER_BY_DAY_OF_WEEK = {v: k for k, v in DAY_OF_WEEK_BY_DAY_NUMBER.items()}

    def __init__(self, lessons: list[Lesson], current_payload: DisplaySchedulePayload) -> None:
        self._current_payload = current_payload
        self._lessons = lessons

    @property
    def message(self) -> str:
        day = self.TEXT_BY_DAY_OF_WEEK[self._current_payload.day]
        day_type = NUMERATOR_TEXT if self._current_payload.is_numerator else DENOMINATOR_TEXT
        date_ = date.today()
        if is_numerator() and not self._current_payload.is_numerator or is_denominator() and self._current_payload.is_numerator:
            date_ += timedelta(days=7)  # +1 неделя
        date_ += timedelta(days=self.DAY_NUMBER_BY_DAY_OF_WEEK[self._current_payload.day])
        title = SCHEDULE_TITLE_MESSAGE.format(day=day, day_type=day_type, date=date_.strftime("%d.%m.%Y"))
        if not self._lessons:
            return f"{title}\n\n{NOT_LESSONS_MESSAGE}"
        message = f"{title}\n\n"
        for lesson in self._lessons:
            message += LESSON_MESSAGE.format(
                lesson_number=lesson.lesson_number,
                start_time=lesson.start_time.strftime("%H:%M"),
                end_time=lesson.end_time.strftime("%H:%M"),
                content="\n".join(lesson.content),
            )
            message += "\n"
        return message

    @property
    def keyboard(self) -> Keyboard:
        return [
            self.day_button(dayofweek=DayOfWeek.MONDAY),
            self.day_button(dayofweek=DayOfWeek.TUESDAY),
            self.day_button(dayofweek=DayOfWeek.WEDNESDAY),
            Row(),
            self.day_button(dayofweek=DayOfWeek.THURSDAY),
            self.day_button(dayofweek=DayOfWeek.FRIDAY),
            self.day_button(dayofweek=DayOfWeek.SATURDAY),
            Row(),
            self.day_button(dayofweek=DayOfWeek.SUNDAY),
            self.back_button(),
            self.next_week_button(),
            Row(),
            ERROR_REPORT_BUTTON
        ]

    def day_button(self, dayofweek: DayOfWeek) -> Button:
        label = self.BUTTON_LABEL_BY_DAY_OF_WEEK[dayofweek]
        payload = self._current_payload.copy()
        payload.day = dayofweek
        color = self.color_by_dayofweek(dayofweek)
        return Button(label=label, payload=payload, color=color)

    def back_button(self) -> Button:
        return Button(
                label=BACK_BUTTON_TEXT,
                payload=ChoiceGroupPayload(**self._current_payload.dict()),
                color=KeyboardButtonColor.PRIMARY)

    def next_week_button(self) -> Button:
        label = CURRENT_WEEK_BUTTON if self._current_payload.is_numerator else NEXT_WEEK_BUTTON
        next_week_payload = self._current_payload.copy()
        next_week_payload.is_numerator = not self._current_payload.is_numerator  # инверсия
        color = KeyboardButtonColor.POSITIVE if self._current_payload.is_numerator else KeyboardButtonColor.PRIMARY
        return Button(label=label, payload=next_week_payload, color=color)

    def color_by_dayofweek(self, dayofweek: DayOfWeek) -> KeyboardButtonColor:
        today = datetime.now().weekday()
        return KeyboardButtonColor.POSITIVE if self.DAY_OF_WEEK_BY_DAY_NUMBER[today] == dayofweek else KeyboardButtonColor.PRIMARY
