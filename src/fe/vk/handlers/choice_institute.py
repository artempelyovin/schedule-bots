from vkbottle.bot import MessageEvent
from vkbottle.dispatch.rules.base import PayloadMapRule
from vkbottle.framework.labeler import BotLabeler
from vkbottle_types.events import GroupEventType

from be.db.models import UserState
from be.managers import InstituteManager
from fe.common.dialogs import ChoiceInstituteDialog
from fe.common.payloads import ChoiceInstitutePayload
from fe.vk.utils import StateFromPayloadRule, generate_vk_keyboard, save_user

labeler = BotLabeler()


@labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    StateFromPayloadRule(UserState.CHOICE_INSTITUTE),
    # PayloadMapRule(ChoiceInstitutePayload.to_map()),
)
@save_user
async def choice_institute_handler(event: MessageEvent):
    payload = ChoiceInstitutePayload(**event.payload)
    institutes = await InstituteManager.get_by_university(university_id=payload.university_id)
    dialog = ChoiceInstituteDialog(institutes=institutes, current_payload=payload)

    await event.edit_message(dialog.message, keyboard=generate_vk_keyboard(dialog.keyboard))
