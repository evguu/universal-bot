import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from abstract.request import ServerBaseRequest
from abstract.server import ServerBase
from logs.log import error_handling_decorator
from servers.VK import config as vk_config
from utils.keyboard_implementer import KeyboardImplementer
from utils.user import User

vk_session = vk_api.VkApi(token=vk_config.token_vk)
vk = vk_session.get_api()


class VKServer(ServerBase, KeyboardImplementer):

    def __init__(self, name):
        ServerBase.__init__(self, name)
        KeyboardImplementer.__init__(self)

    def send_message(self, user, message, reply_to_message_id=None):
        if repr(user) in self.users_keyboards and self.users_keyboards[repr(user)].options:
            vk.messages.send(
                message=message,
                random_id=get_random_id(),
                keyboard=self.users_keyboards[repr(user)].options.get_keyboard(),
                peer_id=user.user_id
            )
            self.users_keyboards[repr(user)].options = None
        else:
            vk.messages.send(
                message=message,
                random_id=get_random_id(),
                peer_id=user.user_id
            )
        ServerBase.send_message(self, user, message, reply_to_message_id)
        return "ok"

    def abstractify_request(self, raw_req):
        print(raw_req)
        if raw_req["type"] == "confirmation":
            return ServerBaseRequest(User(self, 0, 0), "REBIND!")
        user = User(self, raw_req["object"]["user_id"], raw_req["group_id"])
        message = raw_req["object"]["body"]
        if not message:
            return False
        message_id = raw_req["object"]["id"]
        abs_req = ServerBaseRequest(user, message)
        abs_req.message_id = message_id
        print(abs_req)
        return abs_req

    @error_handling_decorator
    def request_received(self, req):
        if not req:
            return "ok"
        if req.message == "REBIND!" and req.user.user_id == 0:
            return vk_config.confirmation_string
        super(VKServer, self).request_received(req)
        return "ok"

    def options_to_buttons(self, user):
        keyboard = VkKeyboard(one_time=True)
        if not self.users_keyboards[repr(user)].options:
            return
        for button in self.users_keyboards[repr(user)].options:
            try:
                keyboard.add_button(button[0], color=VkKeyboardColor.DEFAULT)
            except:
                keyboard.add_line()
                keyboard.add_button(button[0], color=VkKeyboardColor.DEFAULT)
        self.users_keyboards[repr(user)].options = keyboard


server = VKServer("VK")
