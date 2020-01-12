import requests
from flask import jsonify

from abstract.request import ServerBaseRequest
from abstract.server import ServerBase
from logs.log import error_handling_decorator
from logs.log import init_logging_server
from servers.Telegram import config as telegram_config
from utils.exceptions import NoMessageIdToReplyException
from utils.keyboard_implementer import KeyboardImplementer, KeyboardCondition
from utils.user import User

URL = "https://api.telegram.org/bot{}/".format(telegram_config.token_telegram)


class TelegramServer(ServerBase, KeyboardImplementer):

    def __init__(self, name):
        ServerBase.__init__(self, name)
        KeyboardImplementer.__init__(self)

    def send_message(self, user, message, reply_to_message_id=None):
        url = URL + "sendMessage"
        answer = self.form_request(user, message, reply_to_message_id)
        req = requests.post(url, json=answer)
        ServerBase.send_message(self, user, message, reply_to_message_id)
        return req.json()

    def abstractify_request(self, raw_req):
        if "message" in raw_req.keys():
            if "chat" in raw_req["message"].keys() and "text" in raw_req["message"].keys() \
                    and "from" in raw_req["message"].keys():
                user = User(self, raw_req["message"]["from"]["id"], raw_req["message"]["chat"]["id"])
                message = raw_req["message"]["text"]
                is_bot = raw_req["message"]["from"]["is_bot"]
                message_id = raw_req["message"]["message_id"]
            else:
                return
        else:
            return
        if is_bot:
            return

        abs_req = ServerBaseRequest(user, message)
        abs_req.message_id = message_id
        return abs_req

    @error_handling_decorator
    def request_received(self, req):
        if not req:
            return jsonify(success=False)
        super(TelegramServer, self).request_received(req)
        return jsonify(success=True)

    def form_request(self, user, message, reply_to_message_id=None):
        if repr(user) not in self.users_keyboards:
            self.users_keyboards[repr(user)] = KeyboardCondition()

        if not reply_to_message_id:
            if self.users_keyboards[repr(user)].options or self.users_keyboards[repr(user)].is_keyboard_visible:
                raise NoMessageIdToReplyException("Нельзя работать с клавиатурой без message_id!")

        if self.users_keyboards[repr(user)].is_keyboard_visible:
            if not self.users_keyboards[repr(user)].options:
                self.users_keyboards[repr(user)].is_keyboard_visible = False
                answer = {
                    "chat_id": user.dialog_id,
                    "reply_to_message_id": reply_to_message_id,
                    "text": message,
                    "reply_markup": {"remove_keyboard": True,
                                     "selective": True}
                }
            else:
                # Показываем клавиатуру
                self.users_keyboards[repr(user)].is_keyboard_visible = True
                answer = {"chat_id": user.dialog_id,
                          "reply_to_message_id": reply_to_message_id,
                          "text": message,
                          "reply_markup": {"keyboard": self.users_keyboards[repr(user)].options,
                                           "selective": True,
                                           "one_time_keyboard": True}}
                self.users_keyboards[repr(user)].options = None
        else:
            answer = {
                "chat_id": user.dialog_id,
                "text": message,
            }

        return answer


server = TelegramServer("Telegram")
init_logging_server(server)
