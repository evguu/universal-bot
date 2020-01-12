import random

import requests

from apps.apps_router import command_route


def get_btc_to_usd_ratio():
    url = "https://yobit.net/api/3/ticker/btc_usd"
    r = requests.get(url).json()
    price = r["btc_usd"]["high"]
    return price


options = [
    "Очень дорогой, аж {:.1f} USD, но пересдача дороже. 11 студентов группы 972304 подтвердят.",
    "Всего {:.1f} USD, вот писал бы код на двести, а не сто рублей - уже купался бы в этих биткоинах...",
    "Биткоин стоит {:.1f} USD, а сдача зачета - всего 2 гривнi. Сделай правильный выбор.",
    "А вот возьму и не скажу, что стоит он {:.1f} USD. Тьфу...",
    "Кто прочетал тот стоит {:.1f} USD."
]


@command_route(commands=["/btc"],
               args=["server", "req"],
               help_text="Узнать курс биткоина к доллару.")
def _(server, req):
    server.send_message(req.user, random.choice(options).format(get_btc_to_usd_ratio()))
