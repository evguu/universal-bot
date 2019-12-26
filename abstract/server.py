from abc import ABC, abstractmethod
from abstract import request
from logs import log


class AbstractServer(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def send_message(self, user, message, reply_to_message_id=None):
        """
        Отослать сообщение на сервер.
        """
        log.log(user=user, message=message, mode="SM")

    def __repr__(self):
        return "AbstractServer(\"{}\")".format(self.name)

    def __str__(self):
        return self.name

    @abstractmethod
    def request_received(self, req):
        """
        Отослать абстрактный запрос <req> на обработку.

        Аргумент req должен иметь тип AbstractServerRequest.
        """
        log.log(user=req.user, message=req.message, mode="RR")
        request.process_request(self, req)

    @abstractmethod
    def abstractify_request(self, raw_req):
        """
        Преобразует запрос с сервера в абстрактный.
        """
        pass
