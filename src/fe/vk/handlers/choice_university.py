from vkbottle.bot import MessageEvent
from vkbottle.framework.labeler import BotLabeler
from vkbottle_types.events import GroupEventType

from be.db.models import UserState
from be.managers import UniversityManager
from fe.common.dialogs import ChoiceUniversityDialog
from fe.common.payloads import ChoiceUniversityPayload
from fe.vk.utils import PayloadIsPydanticModelRule, StateFromPayloadRule, generate_vk_keyboard, save_user

labeler = BotLabeler()


@labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    StateFromPayloadRule(UserState.CHOICE_UNIVERSITY),
    PayloadIsPydanticModelRule(ChoiceUniversityPayload),
)
@save_user
async def choice_university_handler(event: MessageEvent):
    payload = ChoiceUniversityPayload(**event.payload)
    universities = await UniversityManager.get_all()
    dialog = ChoiceUniversityDialog(universities=universities, current_payload=payload)

    await event.edit_message(dialog.message, keyboard=generate_vk_keyboard(dialog.keyboard))
