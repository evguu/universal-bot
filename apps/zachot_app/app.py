import random

from apps.apps_router import command_route

options = [
    "Отдай 2 гривнi хранителю и сдашь зачет.",
    "Не спорь с Мытником и пересдашь без деканата.",
    "Веди конспект и будет тебе счастье.",
    "Не пытайся списать с телефона ОКП и не отлетишь.",
    "Не пропускай лекции по ИКГ и автомат пополнит твой арсенал."
]


@command_route(commands=["/zachot", "зачет"],
               args=["server", "req"],
               help_text="Узнать тайные техники сдачи зачетов.")
def _(server, req):
    server.send_message(req.user, random.choice(options))
