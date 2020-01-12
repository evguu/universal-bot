from apps.init import init_apps
from apps.apps_router import execute_app
from config import config
from utils.hookers import Hooker
from time import time
from utils.user import User
from database import database

init_apps()


class ServerBaseRequest:
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def __repr__(self):
        return "ServerBaseRequest({}, \"{}\")".format(self.user,
                                                      self.message)


def process_request(server, req: ServerBaseRequest):

    if req.user.banned_until:
        diff = int(req.user.banned_until) - int(time())
        if diff >= 0:
            if req.message[0] == "/":
                server.send_message(req.user, "До окончания бана {} секунд.\nПричина: {}".format(diff,
                                                                                                 req.user.banned_for))
            return
        else:
            # Бан истек
            User.user_data_from_db[req.user.server_user_id][1] = None
            User.user_data_from_db[req.user.server_user_id][2] = None
            database.update_ban_record(None, None, req.user.server_user_id)
            server.send_message(req.user, "Твой бан кончился, больше не нарушай.")

    hooker = Hooker.get_hooker(req.user)
    if hooker:
        try:
            hooker.arg_read(req.message, req.message_id)
        except AttributeError:
            hooker.arg_read(req.message)
        return

    split_message = req.message.split()
    cmd = split_message[0]
    if "@" in cmd:
        if cmd.split("@")[1] != config.bot_username_in_telegram:
            # Если мы в группе и команду шлют не нам, не читаем ее.
            return
        # Если все же нам, игнорируем все что после @.
        cmd = cmd.split("@")[0]

    args = []

    if len(split_message) > 1:
        args = split_message[1:]

    res = execute_app(cmd, server=server, req=req, args=args, cmd=cmd)
    if not res:
        if req.message[0] == "/":
            server.send_message(req.user, "Неизвестная команда.\n"
                                          "Используйте /help для получения списка команд.")
