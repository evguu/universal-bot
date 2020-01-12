from apps.apps_router import command_route
from utils.hooker_decorator import multipart_input
from utils.hookers import HookerArgData
from time import time
from datetime import datetime
from database import database
from utils.user import User


@command_route(commands=["/ban"],
               args=["req", "args"],
               help_text="Забанить пользователя.",
               permission_required=["Owner"])
def _(req, args):
    @multipart_input(req, args,
                     HookerArgData(
                         lambda x: "@" in x,
                         "Введите suid пользователя."
                     ),
                     HookerArgData(
                         lambda x: x.isdigit() and int(x) > 0,
                         "Введите продолжительность бана в секундах."
                     ),
                     HookerArgData(
                         lambda x: len(x) <= 100,
                         "Введите причину бана.",
                         options=[
                             ["Флуд"],
                             ["Оскорбление администрации"]
                         ],
                         greedy=True
                     )
                     )
    def _(suid, duration, reason):
        if suid == "@":
            suid = req.user.server_user_id

        # Если заданный пользователь существует, но не загружен, загружаем его.
        if suid not in User.user_data_from_db:
            User(*suid.split("@"), 0)

        now = int(time())
        until = now + int(duration)

        User.user_data_from_db[suid][1] = until
        User.user_data_from_db[suid][2] = reason
        database.update_ban_record(until, reason, suid)
        return "Пользователь {} забанен до {}.\n" \
               "Причина: {}".format(suid, datetime.fromtimestamp(until), reason)


@command_route(commands=["/pardon"],
               args=["req", "args"],
               help_text="Разбанить пользователя.",
               permission_required=["Owner"])
def _(req, args):
    @multipart_input(req, args,
                     HookerArgData(
                         lambda x: "@" in x,
                         "Введите suid пользователя."
                     ))
    def _(suid):
        if suid == "@":
            suid = req.user.server_user_id

        # Если заданный пользователь существует, но не загружен, загружаем его.
        if suid not in User.user_data_from_db:
            User(*suid.split("@"), 0)

        User.user_data_from_db[suid][1] = None
        User.user_data_from_db[suid][2] = None
        database.update_ban_record(None, None, suid)
        return "Пользователь {} разбанен.".format(suid)
