from config import config
from apps.apps_router import execute_app
from utils.hookers import Hooker


class AbstractServerRequest:
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def __repr__(self):
        return "AbstractServerRequest({}, \"{}\")".format(self.user,
                                                          self.message)


def process_request(server, req: AbstractServerRequest):
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
    if not execute_app(cmd, server=server, req=req, args=args, cmd=cmd):
        if cmd == "/testcrash":
            from utils.exceptions import TestException
            raise TestException("Проверочное исключение.")
        elif req.message[0] == "/":
            server.send_message(req.user, "Неизвестная команда.\n"
                                          "Используйте /help для получения списка команд.")
