from datetime import date


def is_numerator() -> bool:  # TODO(issue-1): add unit tests
    """
    Определяем является ли текущая неделя числителем.
    Все чётные недели года - числители, все нечётные - знаменатели
    """
    today = date.today()
    week_number = today.isocalendar()[1]  # формат: (год, номер недели, номер дня недели)
    return week_number % 2 == 0


def is_denominator() -> bool:   # TODO(issue-1): add unit tests
    return not is_numerator()
