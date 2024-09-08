from vkbottle.bot import MessageEvent
from vkbottle.dispatch.rules.base import PayloadMapRule
from vkbottle.framework.labeler import BotLabeler
from vkbottle_types.events import GroupEventType

from be.db.models import UserState
from be.managers import GroupManager
from fe.common.dialogs import ChoiceCourseDialog
from fe.common.payloads import ChoiceCoursePayload
from fe.vk.utils import StateFromPayloadRule, generate_vk_keyboard, save_user

labeler = BotLabeler()


@labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    StateFromPayloadRule(UserState.CHOICE_COURSE),
    # PayloadMapRule(ChoiceCoursePayload.to_map()),
)
@save_user
async def choice_course_handler(event: MessageEvent):
    payload = ChoiceCoursePayload(**event.payload)
    courses_info = await GroupManager.get_courses_info_by_institute(institute_id=payload.institute_id)
    dialog = ChoiceCourseDialog(courses_info=courses_info, current_payload=payload)

    await event.edit_message(dialog.message, keyboard=generate_vk_keyboard(dialog.keyboard))
