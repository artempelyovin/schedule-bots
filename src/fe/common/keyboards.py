from typing import Any, TypeAlias

from pydantic import BaseModel
from vkbottle import KeyboardButtonColor

from fe.common.constants import LEFT_BUTTON_TEXT, RIGHT_BUTTON_TEXT
from fe.common.payloads import PaginationPayload


class Button(BaseModel):
    label: str
    payload: dict[str, Any]
    color: KeyboardButtonColor  # пока чисто для VK


class Row(BaseModel):  # тупо класс-маркер, сигнализирующий о переносе клавиш на новую строку
    pass


Keyboard: TypeAlias = list[Button | Row]


def _generate_pagination_keyboard(
    current_payload: PaginationPayload,
    buttons: list[Button],
    back_button: Button,
    error_report_button: Button,
) -> Keyboard:
    """
    Генерирует клавиатуру из 10 кнопок (ограничение VK для inline клавиатур) формате:
        [   button_1   ] [   button_2   ] [  button_3    ]
        [   button_4   ] [   button_5   ] [   button_6   ]
        [      <<      ] [  back_button ] [      >>      ]
        [              error_report_button               ]
    """
    offset = current_payload.offset
    if len(buttons) <= 6:  # тупо нечего двигать, всё убирается на одной странице:)  # noqa: PLR2004
        prevision_offset = 0
        next_offset = 0
    else:
        prevision_offset = offset - 6 if offset >= 6 else 0  # noqa: PLR2004
        next_offset = offset + 6 if offset + 6 < len(buttons) else len(buttons) - offset

    left_button_color = KeyboardButtonColor.SECONDARY if offset == 0 else KeyboardButtonColor.PRIMARY
    right_button_color = KeyboardButtonColor.SECONDARY if len(buttons) - offset < 6 - 1 else KeyboardButtonColor.PRIMARY

    left_payload = current_payload.copy()
    left_payload.offset = prevision_offset
    right_payload = current_payload.copy()
    right_payload.offset = next_offset

    raw_keyboard: Keyboard = [
        *buttons[offset : offset + 3],  # первые 3 кнопки
        Row(),
        *buttons[offset + 3 : offset + 6],  # вторые 3 кнопки
        Row(),
        Button(label=LEFT_BUTTON_TEXT, payload=left_payload.dict(), color=left_button_color),
        back_button,
        Button(label=RIGHT_BUTTON_TEXT, payload=right_payload.dict(), color=right_button_color),
        Row(),
        error_report_button,
    ]

    # Удаляем подряд идущие  Row(), т.к. выше они могут сгенерироваться:(
    keyboard: Keyboard = []
    for item in raw_keyboard:
        if keyboard and isinstance(keyboard[-1], Row) and isinstance(item, Row):
            continue
        keyboard.append(item)
    return keyboard
