from apps.apps_router import command_route
import random

options = [
    "Я запрещаю вам switch.",
    "Я запрещаю вам забивать очередь.",
    "Я запрещаю вам сдавать с первого раза.",
    "Я запрещаю вам возвращать значения из функций.",
    "Я запрещаю вам описывать структуры в блок-схеме.",
    "Я запрещаю вам сдавать шестую лабу в двух частях.",
    "Я запрещаю вам string.h!",
    "Я запрещаю вам malloc.",
    "Я запрещаю вам шрифт размером в полпикселя!",
    "Я запрещаю вам C++."
]


@command_route(commands=["/laba", "/switch"],
               args=["server", "req"],
               help_text="Спросить у Бутова по поводу сдачи лабораторной.")
def execute(server, req):
    server.send_message(req.user, random.choice(options))
