import threading
from time import sleep

from apps.apps_router import command_route
from utils.hooker_decorator import multipart_input
from utils.hookers import HookerArgData


@command_route(commands=["/repeat"],
               args=["server", "req", "args"],
               help_text="Повторить сообщение через заданное число секунд (1 - 60).")
def _(server, req, args):
    def arg1_validator(x):
        return 1 <= int(x) <= 60

    @multipart_input(req, args,
                     HookerArgData(arg1_validator,
                                   "Введите время ожидания в секундах (1 - 60).",
                                   options=[["1"],
                                            ["5"],
                                            ["20"],
                                            ["60"]]),
                     HookerArgData(lambda x: True,
                                   "Введите ваше сообщение.",
                                   greedy=True))
    def _(delay, msg):
        delay = int(delay)

        def target():
            sleep(delay)
            server.send_message(req.user, "Ваше отложенное сообщение:\n\n" + msg)

        threading.Thread(target=target).start()

        return "Сообщение отложено на {} секунд.".format(delay)
