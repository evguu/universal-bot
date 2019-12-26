from abstract.server import AbstractServer
from abstract.request import AbstractServerRequest
from utils.user import User
from flask import jsonify
from servers.Telegram import config as telegram_config
import requests
from utils.mixins import KeyboardMixin
from logs.log import error_handling_decorator
from logs.log import init_logging_server

URL = "https://api.telegram.org/bot{}/".format(telegram_config.token_telegram)


class TelegramServer(AbstractServer, KeyboardMixin):

    def __init__(self, name):
        AbstractServer.__init__(self, name)
        KeyboardMixin.__init__(self)

    def send_message(self, user, message, reply_to_message_id=None):
        url = URL + "sendMessage"
        answer = KeyboardMixin.form_request(self, user, message, reply_to_message_id)
        req = requests.post(url, json=answer)
        AbstractServer.send_message(self, user, message, reply_to_message_id)
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

        abs_req = AbstractServerRequest(user, message)
        abs_req.message_id = message_id
        return abs_req

    @error_handling_decorator
    def request_received(self, req):
        if not req:
            return jsonify(success=False)
        super(TelegramServer, self).request_received(req)
        return jsonify(success=True)


server = TelegramServer("Telegram")
init_logging_server(server)
