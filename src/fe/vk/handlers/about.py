from vkbottle.bot import MessageEvent
from vkbottle.framework.labeler import BotLabeler
from vkbottle_types.events import GroupEventType

from be.db.models import UserState
from fe.common.dialogs import AboutBotDialog
from fe.vk.utils import StateFromPayloadRule, generate_vk_keyboard, save_user

labeler = BotLabeler()
dialog = AboutBotDialog()


@labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    StateFromPayloadRule(UserState.ABOUT_BOT),
)
@save_user
async def about_bot_handler(event: MessageEvent):
    await event.edit_message(dialog.message, keyboard=generate_vk_keyboard(dialog.keyboard))
