import datetime
from config import config
import requests
from utils.hookers import Hooker, HookerArgData
from apps.apps_router import command_route


def is_valid_group_number(group: str):
    """
    Checks parameter for possibility to be group number.
    Group number must be a 6 (or less) digit string.
    """
    if type(group) != str:
        return False
    if len(group) != 6:
        return False
    if not group.isdigit():
        return False
    if not 0 < int(group) < 10**6:
        return False
    return True


OUTPUT_MODE_TODAY_FULL = 0  # Все сегодняшние пары
OUTPUT_MODE_TODAY_CURRENT = 1  # Текущая пара (или следующая, если перерыв, или пусто если сегодня все
OUTPUT_MODE_TODAY_LEFT = 2  # Оставшиеся на сегодня пары, включая текущую
OUTPUT_MODE_TOMORROW = 3  # Завтрашние пары


def parse_schedule(schedule, output_mode, subgroup):
    """
    Преобразует расписание-JSON в читабельный формат

    :param schedule: JSON с расписанием.
    :param output_mode: Режим вывода (сейчас, осталось и т.д.).
    :param subgroup: Подгруппа запрашивающего (пока не используется).
    :return: Читабельная форма расписания.
    """
    sum_result = ""
    time_now = datetime.datetime.now()
    time_now = (time_now.hour + config.time_offset) * 60 + time_now.minute

    t_l_end = 0

    for lesson in schedule:
        l_start, l_end = lesson["lessonTime"].split("-")
        l_start = l_start.split(":")
        l_end = l_end.split(":")
        l_start = int(l_start[0]) * 60 + int(l_start[1])
        l_end = int(l_end[0]) * 60 + int(l_end[1])

        if output_mode == OUTPUT_MODE_TODAY_CURRENT:
            if not l_start <= time_now <= l_end:
                if not t_l_end <= time_now <= l_start:
                    t_l_end = l_end
                    continue
                else:
                    t_l_end = l_end

        if output_mode == OUTPUT_MODE_TODAY_LEFT:
            if not l_start <= time_now <= l_end:
                if not t_l_end <= time_now <= l_start:
                    t_l_end = l_end
                    continue
                else:
                    t_l_end = l_end

        # Если номер подгруппы совпадает или если пара для всей группы
        if lesson["numSubgroup"] == subgroup or not lesson["numSubgroup"]:
            result = "Предмет: {}\n"\
                     "Тип предмета: {}\n" \
                     "Время: {}\n".format(lesson["subject"],
                                          lesson["lessonType"],
                                          lesson["lessonTime"])
            if lesson["numSubgroup"]:
                result += "Подгруппа: {}\n".format(lesson["numSubgroup"])
            if lesson["note"] is not None:
                result += "Примечание: {}\n".format(lesson["note"])
            for auditory in lesson["auditory"]:
                result += "Аудитория: {}\n".format(auditory)
            for employee in lesson["employee"]:
                result += "Преподаватель: {} {} {}\n".format(employee["lastName"],
                                                             employee["firstName"],
                                                             employee["middleName"])
            sum_result += result + "\n"
    if not sum_result:
        return "Пар не найдено. Иди спи!"
    sum_result = sum_result[:-2]  # Убираем лишние строки в конце
    return sum_result


def get_schedule(group, mode=OUTPUT_MODE_TODAY_FULL, subgroup=0):
    """
    Запрашивает JSON расписаниие с сайта, отправляет на обработку и выводит результат.

    :param group: Группа студента.
    :param mode: Режим вывода (сейчас, осталось и т.д.)
    :param subgroup: Подгруппа студента.
    :return: Готовое к выводу ботом расписание.
    """

    url = "https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup=" + group
    try:
        r = requests.get(url)
        if mode == OUTPUT_MODE_TODAY_FULL:
            return "Расписание на сегодня:\n" + parse_schedule(r.json()["todaySchedules"], mode, subgroup)
        if mode == OUTPUT_MODE_TODAY_CURRENT:
            return "Текущая/следующая пара:\n" + parse_schedule(r.json()["todaySchedules"], mode, subgroup)
        if mode == OUTPUT_MODE_TODAY_LEFT:
            return "Оставшиеся на сегодня пары:\n" + parse_schedule(r.json()["todaySchedules"], mode, subgroup)
        return "Расписание на завтра:\n" + parse_schedule(r.json()["tomorrowSchedules"], mode, subgroup)
    except Exception as e:
        print(e)
        return "Возникла ошибка при обработке запроса. Возможно, запрашиваемый сайт временно недоступен или вы ввели " \
               "некорректные данные. "


@command_route(commands=["/schedule"],
               args=["req", "args"],
               help_text="Узнать расписание группы.")
def execute(req, args):
    def hooker_done(group, mode):
        if mode == "сегодня":
            return get_schedule(group, OUTPUT_MODE_TODAY_FULL)
        elif mode == "сейчас":
            return get_schedule(group, OUTPUT_MODE_TODAY_CURRENT)
        elif mode == "осталось":
            return get_schedule(group, OUTPUT_MODE_TODAY_LEFT)
        elif mode == "завтра":
            return get_schedule(group, OUTPUT_MODE_TOMORROW)
        else:
            return "Некорректный запрос."

    def arg1_validator(x):
        return is_valid_group_number(x)

    def arg2_validator(x):
        return x in ("сегодня", "сейчас", "осталось", "завтра")

    hooker = Hooker(req.user, hooker_done,
                    HookerArgData(arg1_validator,
                                  "Введите номер группы.",
                                  options=[["972304"]]),
                    HookerArgData(arg2_validator,
                                  "Выберите режим.",
                                  options=[["сегодня"],
                                           ["сейчас"],
                                           ["осталось"],
                                           ["завтра"]]))
    if len(args):
        for arg in args:
            try:
                hooker_response = hooker.arg_read(arg, message_id=req.message_id, presend=True)
            except AttributeError:
                hooker_response = hooker.arg_read(arg, presend=True)
            if not hooker_response:
                return

    hooker.init(req.message_id)
