from utils.hookers import HookerArgData, Hooker
from utils.user import User
from config import config
from apps.apps_router import command_route


def send_feedback(user, text):
    from servers.Telegram.server import server as telegram_server
    telegram_server.send_message(User(telegram_server,
                                      0,
                                      config.feedback_chat_id),
                                 "<{}> {}".format(user, text))


@command_route(commands=["/feedback"],
               args=["req", "args"],
               help_text="Отправить сообщение разработчику. Флудеры будут наказаны!")
def execute(req, args):
    def hooker_done(msg):
        send_feedback(req.user, msg)
        return "Сообщение отправлено администратору."

    def arg1_validator(x):
        return len(x)

    hooker = Hooker(req.user, hooker_done,
                    HookerArgData(arg1_validator,
                                  "Введите сообщение."))
    if len(args):
        try:
            hooker_response = hooker.arg_read(" ".join(args), message_id=req.message_id, presend=True)
        except AttributeError:
            hooker_response = hooker.arg_read(" ".join(args), presend=True)
        if not hooker_response:
            return
    hooker.init(req.message_id)
