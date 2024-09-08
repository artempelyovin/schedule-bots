from fe.vk.handlers import (
    about,
    choice_course,
    choice_group,
    choice_institute,
    choice_university,
    display_schedule,
    error_report,
    start,
)

labelers = [
    start.labeler,
    about.labeler,
    choice_university.labeler,
    choice_institute.labeler,
    choice_course.labeler,
    choice_group.labeler,
    display_schedule.labeler,
    error_report.labeler,
]

__all__ = ["labelers"]
