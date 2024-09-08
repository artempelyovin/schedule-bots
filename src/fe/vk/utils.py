import logging
from typing import Callable

from vkbottle import ABCRule, Callback
from vkbottle import Keyboard as VkKeyboard
from vkbottle.tools.dev.mini_types.base import BaseMessageMin
from vkbottle.tools.dev.mini_types.bot import MessageEventMin

from be.db.models import VK, UserState
from be.managers import UserManager
from fe.common.keyboards import Button, Keyboard, Row
from fe.vk.config import api

logger = logging.getLogger(__name__)


def generate_vk_keyboard(keyboard: Keyboard) -> str:
    vk_keyboard = VkKeyboard(inline=True)
    for object_ in keyboard:
        if isinstance(object_, Button):
            vk_keyboard.add(Callback(label=object_.label, payload=object_.payload), color=object_.color)
        elif isinstance(object_, Row):
            vk_keyboard.row()
        else:
            raise ValueError(f"Получен неизвестный тип {type(object_)} при формировании VK клавиатуры")
    return vk_keyboard.get_json()


class StateFromPayloadRule(ABCRule[BaseMessageMin]):
    def __init__(self, state: UserState):
        self.state = state

    async def check(self, event: BaseMessageMin) -> bool:
        if not event.payload or "state" not in event.payload:
            return False
        return event.payload["state"] == self.state


def save_user(func: Callable[[MessageEventMin], ...]) -> Callable[[MessageEventMin], ...]:
    async def async_wrapper(event: MessageEventMin) -> None:
        def get_state_from_payload(payload: dict | None) -> UserState:
            if not payload or "state" not in payload:
                return UserState.UNKNOWN
            return UserState(payload["state"])

        new_payload = event.payload
        new_state = get_state_from_payload(new_payload)

        user = await UserManager.get(user_id=event.peer_id, messenger=VK)
        if not user:
            vk_user = (await api.users.get(user_ids=[event.peer_id]))[0]
            user = await UserManager.add(
                user_id=event.peer_id,
                username=None,  # не приходит для VK :(
                first_name=vk_user.first_name,
                last_name=vk_user.last_name,
                messenger=VK,
                state=new_state,
                payload=new_payload,
            )
            logger.info(f"Add user {user} to the database")
        else:
            old_state = user.state
            old_payload = user.payload
            if old_state != new_state or old_payload != new_payload:
                updated_user = await UserManager.update_state_and_payload(
                    user_id=event.peer_id,
                    messenger=VK,
                    state=new_state,
                    current_payload=new_payload,
                )
                logger.info(f"Updated user from {user} to {updated_user}")
        await func(event)

    return async_wrapper
