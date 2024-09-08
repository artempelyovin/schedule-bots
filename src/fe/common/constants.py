# ============================================================
# ========================== Команды =========================
# ============================================================
START_DIALOG_COMMANDS = ["/start", "start", "/старт", "старт"]


# ============================================================
# ====================== Текст сообщений =====================
# ============================================================
_START_MESSAGE = """
✨Вас приветствует "Бот Расписания ВлГУ"!✨

➖Для начала работы выберите свой институт и группу

➖После выбора группы Вам будут доступны кнопки с ежедневным расписанием. Зелёная кнопка - текущий день недели.

P.S: Обращайте внимание на числитель/знаменатель

➖Нашли ошибку? Нажмите кнопку "Сообщить об ошибке"

⚡Создатели:
{creator_link} - разработчик бота (по всем вопросам в ЛС)
"""

VK_START_MESSAGE = _START_MESSAGE.format(creator_link="@id258430252 (Артём Пелёвин)")
TELEGRAM_START_MESSAGE = _START_MESSAGE.format(creator_link="@artempelyovin")

ABOUT_BOT_MESSAGE = """
TODO
"""

ERROR_REPORT_MESSAGE = """
Нашли какую то ошибку или недочёт?

Пожалуйста, напишите ниже детальное сообщение об проблеме.
Сообщение будет отправлено разработчикам, они обязательно его прочтут!
Спасибо :)
"""

THANKS_FOR_ERROR_REPORT = """
Спасибо за Ваш отчёт о проблеме:)
Мы обязательно его изучим!
"""

CHOICE_UNIVERSITY_MESSAGE = "Выберите университет ({start}-{stop} из {total}):"
CHOICE_INSTITUTE_MESSAGE = "Выберите институт ({start}-{stop} из {total}):"
CHOICE_COURSE_MESSAGE = "Выберите курс ({start}-{stop} из {total}):"
CHOICE_GROUP_MESSAGE = "Выберите группу ({start}-{stop} из {total}):"
SCHEDULE_TITLE_MESSAGE = "{day_type} {day} ({date})"
LESSON_MESSAGE = """➖ {lesson_number} пара ({start_time} - {end_time})
{content}
"""
NOT_LESSONS_MESSAGE = "➖ Нет пар❗"
MONDAY_TEXT = "Понедельник"
TUESDAY_TEXT = "Вторник"
WEDNESDAY_TEXT = "Среда"
THURSDAY_TEXT = "Четверг"
FRIDAY_TEXT = "Пятница"
SATURDAY_TEXT = "Суббота"
SUNDAY_TEXT = "Воскресенье"
NUMERATOR_TEXT = "⚪"
DENOMINATOR_TEXT = "🟡"


# =============================================
# =============== Текст кнопок ================
# =============================================
FIND_SCHEDULE_BUTTON_TEXT = "Найти расписание"
ABOUT_BOT_BUTTON_TEXT = "О боте"
ERROR_REPORT_BUTTON_TEXT = "Сообщить об ошибке"
BACK_BUTTON_TEXT = "Назад"
LEFT_BUTTON_TEXT = "←"
RIGHT_BUTTON_TEXT = "→"
UNIVERSITY_BUTTON_TEXT = "{university}"
INSTITUTE_BUTTON_TEXT = "{institute}"
COURSE_BUTTON_TEXT = "{course} курс"
COURSE_MAGISTRACY_BUTTON_TEXT = "{course} курс (магистратура)"
GROUP_BUTTON_TEXT = "{group}"
NEXT_WEEK_BUTTON = "Следующая неделя"
CURRENT_WEEK_BUTTON = "Текущая неделя"
MONDAY_BUTTON_TEXT = "Понедельник"
TUESDAY_BUTTON_TEXT = "Вторник"
WEDNESDAY_BUTTON_TEXT = "Среда"
THURSDAY_BUTTON_TEXT = "Четверг"
FRIDAY_BUTTON_TEXT = "Пятница"
SATURDAY_BUTTON_TEXT = "Суббота"
SUNDAY_BUTTON_TEXT = "Воскресенье"
