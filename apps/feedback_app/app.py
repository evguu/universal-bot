from apps.apps_router import command_route
from config import config
from utils.hooker_decorator import multipart_input
from utils.hookers import HookerArgData
from utils.user import User


def send_feedback(user, text):
    from servers.Telegram.server import server as telegram_server
    telegram_server.send_message(User(telegram_server,
                                      0,
                                      config.feedback_chat_id),
                                 "<{}> {}".format(user, text))


@command_route(commands=["/feedback"],
               args=["req", "args"],
               help_text="Отправить сообщение разработчику. Флудеры будут наказаны!")
def _(req, args):
    @multipart_input(req, args,
                     HookerArgData(lambda x: True,
                                   "Введите сообщение.",
                                   greedy=True))
    def _(msg):
        send_feedback(req.user, msg)
        return "Сообщение отправлено администратору."
