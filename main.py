from flask import Flask
from flask import request
from flask_sslify import SSLify

from servers.Telegram import config as telegram_config
from servers.Telegram.server import server as telegram_server
from servers.VK import config as VK_config
from servers.VK.server import server as vk_server

app = Flask(__name__)
sslify = SSLify(app)


@app.route(telegram_config.telegram_path, methods=["POST", "GET"])
def telegram_listener():
    if request.method == "POST":
        req = request.get_json()
        abs_req = telegram_server.abstractify_request(req)

        res = telegram_server.request_received(abs_req)
        if res:
            return res
        else:
            return "Rip"


@app.route(VK_config.vk_path, methods=["POST", "GET"])
def vk_listener():
    if request.method == "POST":
        req = request.get_json()
        abs_req = vk_server.abstractify_request(req)
        if not abs_req:
            return "ok"
        res = vk_server.request_received(abs_req)
        if res:
            return res
        else:
            # ВК будет считать что запрос не дошел, если не отправить ok.
            return "ok"


if __name__ == '__main__':
    app.run()
