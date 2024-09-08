from vkbottle.bot import MessageEvent
from vkbottle.dispatch.rules.base import PayloadMapRule
from vkbottle.framework.labeler import BotLabeler
from vkbottle_types.events import GroupEventType

from be.db.models import UserState
from be.managers import LessonManager
from fe.common.dialogs import DisplayScheduleDialog
from fe.common.payloads import DisplaySchedulePayload
from fe.vk.utils import StateFromPayloadRule, generate_vk_keyboard, save_user

labeler = BotLabeler()


@labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    StateFromPayloadRule(UserState.DISPLAY_SCHEDULE),
    # PayloadMapRule(DisplaySchedulePayload.to_map()),
)
@save_user
async def display_schedule_handler(event: MessageEvent):
    payload = DisplaySchedulePayload(**event.payload)
    lessons = await LessonManager.get_lessons(
        group_id=payload.group_id, day=payload.day, is_numerator=payload.is_numerator
    )
    dialog = DisplayScheduleDialog(lessons=lessons, current_payload=payload)

    await event.edit_message(dialog.message, keyboard=generate_vk_keyboard(dialog.keyboard))
