from vkbottle.bot import MessageEvent
from vkbottle.framework.labeler import BotLabeler
from vkbottle_types.events import GroupEventType

from be.db.models import UserState
from fe.common.dialogs import ErrorReportDialog
from fe.vk.utils import StateFromPayloadRule, generate_vk_keyboard, save_user

labeler = BotLabeler()
dialog = ErrorReportDialog()


@labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    StateFromPayloadRule(UserState.ERROR_REPORT),
)
@save_user
async def error_report_handler(event: MessageEvent):
    await event.edit_message(dialog.message, keyboard=generate_vk_keyboard(dialog.keyboard))
