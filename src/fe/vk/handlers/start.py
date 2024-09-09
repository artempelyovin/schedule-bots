from vkbottle.bot import Message, MessageEvent
from vkbottle.framework.labeler import BotLabeler
from vkbottle_types.events import GroupEventType

from be.db.models import UserState
from fe.common.constants import START_DIALOG_COMMANDS
from fe.common.dialogs import StartDialog
from fe.common.payloads import StartPayload
from fe.vk.utils import PayloadIsPydanticModelRule, StateFromPayloadRule, generate_vk_keyboard, save_user

labeler = BotLabeler()
start_dialog = StartDialog()


@labeler.message(text=START_DIALOG_COMMANDS)
@save_user
async def start_handler(message: Message):
    await message.answer(start_dialog.message, keyboard=generate_vk_keyboard(start_dialog.keyboard))


@labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    StateFromPayloadRule(UserState.START),
    PayloadIsPydanticModelRule(StartPayload),
)
@save_user
async def return_to_start_handler(event: MessageEvent):
    await event.edit_message(start_dialog.message, keyboard=generate_vk_keyboard(start_dialog.keyboard))
