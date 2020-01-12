import functools
import os
import sys
import traceback
from datetime import datetime

from config import config as global_config
from logs import config as logs_config
from utils.user import User

logging_server = None


def init_logging_server(server):
    global logging_server
    logging_server = server


def error_handling_decorator(func):
    @functools.wraps(func)
    def process_exception(self, abs_req):
        try:
            return func(self, abs_req)
        except:
            error_log = "Пользователь: {}\n" \
                        "Сообщение: {}\n" \
                        "Тип ошибки: {}\n" \
                        "Получено исключение:\n{}\n" \
                        "Traceback:\n{}".format(abs_req.user.id, abs_req.message,
                                                type(sys.exc_info()[1]).__name__, sys.exc_info()[1],
                                                "\n".join(traceback.format_tb(sys.exc_info()[2])))
            log(abs_req.user, error_log, "ERR")
            self.send_message(abs_req.user, "Упс! Что-то пошло не так...\n"
                                            "Разработчик уже поставлен в известность.")
            if logging_server:
                logging_server.send_message(
                    User(
                        logging_server,
                        global_config.owner_id,
                        global_config.errors_chat_id),
                    error_log)
            return False

    return process_exception


def log(user, message, mode):
    row_length_max = logs_config.row_length_max
    row_count_max = logs_config.row_count_max
    res = ""
    has_added_period_in_column = False
    if message is not None:
        for num_line in enumerate(message.split("\n")):
            num, line = num_line
            if len(message.split("\n")) > 2 * row_count_max:
                if row_count_max <= num < len(message.split("\n")) - row_count_max:
                    if not has_added_period_in_column:
                        has_added_period_in_column = True
                        res += "    {" + str(len(message.split("\n")) - 2 * row_count_max) + "}\n"
                    continue
            if len(line) > 2 * row_length_max:
                line = line[0:row_length_max] + "{" + str(len(line) - 2 * row_length_max) + "}" + \
                       line[len(line) - row_length_max:len(line)]
            res += "    " + line + "\n"
    else:
        res = "!!NONE!!"

    if mode == "ERR":
        with open(os.path.join(logs_config.error_logs_dir, "log" + datetime.now().strftime("%d%m%y") + ".log"), "a+",
                  encoding="utf8") as f:
            f.write("[{} {}]<{}>\n{}".format(mode, datetime.now().strftime("%d%m%y %H%M%S"), user, message))
    else:
        with open(os.path.join(logs_config.message_logs_dir, "log" + datetime.now().strftime("%d%m%y") + ".log"), "a+",
                  encoding="utf8") as f:
            f.write("[{} {}]<{}>\n{}".format(mode, datetime.now().strftime("%d%m%y %H%M%S"), user, res))
