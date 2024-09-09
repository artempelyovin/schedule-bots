from vkbottle.bot import MessageEvent
from vkbottle.framework.labeler import BotLabeler
from vkbottle_types.events import GroupEventType

from be.db.models import UserState
from be.managers import GroupManager
from fe.common.dialogs import ChoiceGroupDialog
from fe.common.payloads import ChoiceGroupPayload
from fe.vk.utils import StateFromPayloadRule, generate_vk_keyboard, save_user

labeler = BotLabeler()


@labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    StateFromPayloadRule(UserState.CHOICE_GROUP),
)
@save_user
async def choice_group_handler(event: MessageEvent):
    payload = ChoiceGroupPayload(**event.payload)
    groups = await GroupManager.get_by_institute_and_course(
        institute_id=payload.institute_id, course=payload.course, is_magistracy=payload.is_magistracy
    )
    dialog = ChoiceGroupDialog(groups=groups, current_payload=payload)
    await event.edit_message(dialog.message, keyboard=generate_vk_keyboard(dialog.keyboard))
