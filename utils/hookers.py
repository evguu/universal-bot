from utils.mixins import KeyboardMixin


class HookerArgData:
    """
    Совокупность данных, необходимых для запроса аргумента.

    Включает в себя подсказку для пользователя и валидатор введенного аргумента.
    """

    def __init__(self, validator, request_message, options=None):
        """

        :param validator: Функция, проверяющая аргумент на корректность.
        :param request_message: Сообщение, выводимое при запросе аргумента.
        """
        self.validator = validator
        self.request_message = request_message
        self.options = options


class HookerArgPathway:
    """
    На случай, если нам нужно требовать разные аргументы в зависимости от ввода пользователя.

    Содержит список из кортежей экземпляров HookerArgData и функций-валидаторов их выбора.
    """

    def __init__(self, paths):
        self.paths = paths

    def choose_path(self, known_args):
        for path in self.paths:
            # Вернуть первый хукер, который соответствует собранным параметрам
            if path[1](known_args):
                return path[0]
        raise ValueError("Нет правильных путей!!!")


class Hooker:
    """
    Позволяет заполнять функцию аргументами и только после этого выполнять.

    Каждый аргумент проверяется валидатором.
    Пока функция в процессе заполнения, программа может продолжать исполняться.
    """

    # Словарь незакрытых хукеров. В качестве ключей выступают !!текстовые!! user "повесившего".
    # Т.к. один user физически не может повесить более одного хукера, нет необходимости хранить списки.
    hookers = {}

    def __init__(self, user, func, *func_args):
        """
        Создает хукер и запрашивает первый аргумент.

        :param user: Вызвавший пользователь.
        :param func: Функция, которая ожидает параметров.
        :param func_args: Должны быть экземплярами класса HookerArgData.
        """
        self.user = user
        self.func = func
        self.func_args = list(func_args)
        self.received_args = []
        Hooker.hookers[str(user)] = self

    def init(self, message_id=None):
        if len(self.func_args) != 0:
            if isinstance(self.user.server, KeyboardMixin):
                self.user.server.set_options(self.user, self.func_args[0].options)
            self.user.server.send_message(self.user, self.func_args[0].request_message,
                                          reply_to_message_id=message_id)
            if not isinstance(self.user.server, KeyboardMixin) and self.func_args[0].options:
                self.user.server.send_message(self.user,
                                              "Варианты:\n" + "\n".join([i[0] for i in self.func_args[0].options]),
                                              reply_to_message_id=message_id)

    def arg_read(self, message, message_id=None, presend=False):
        """
        Считывает аргумент в хукер, исполняем функцию если он заполнится, или снимаем хукер при неверном аргументе.

        :param message: Данные от пользователя
        :param message_id: ID сообщения, на которое отвечаем
        :param presend: Посылается ли данный параметр до инициализации хукера
        :return: Возвращает валидность сообщения если presend == True
        """

        if message == "--Отмена--":
            self.user.server.send_message(self.user, "Исполнение команды отменено.", reply_to_message_id=message_id)
            self.func_args = []
            return True

        # Аргумент получен и прошел проверку валидатором.
        if self.func_args[0].validator(message):

            # Запоминаем полученный аргумент
            self.received_args.append(message)
            self.func_args.pop(0)

            # Если есть еще аргументы, просим их (если не предотправка).
            # Прошлый аргумент больше не первый, это важно!

            # Аргументов не осталось, выполняем функцию
            if len(self.func_args) == 0:
                if not message_id:
                    message_id = 0
                self.user.server.send_message(self.user, self.func(*self.received_args),
                                              reply_to_message_id=message_id)

                if presend:
                    return True

            # Еще есть аргументы, просим их.
            else:

                if presend:
                    return True

                next_arg = self.func_args[0]

                if isinstance(next_arg, HookerArgPathway):
                    self.func_args[0] = next_arg.choose_path(self.received_args)
                    next_arg = self.func_args[0]

                if isinstance(self.user.server, KeyboardMixin):
                    self.user.server.set_options(self.user, next_arg.options)
                self.user.server.send_message(self.user, next_arg.request_message,
                                              reply_to_message_id=message_id)
                if not isinstance(self.user.server, KeyboardMixin) and self.func_args[0].options:
                    self.user.server.send_message(self.user,
                                                  "Варианты:\n" + "\n".join([i[0] for i in next_arg.options]),
                                                  reply_to_message_id=message_id)

        # Проверка валидатором не пройдена. Пишем об ошибке и удаляем хукер.
        else:

            self.user.server.send_message(self.user, "Введенные вами данные не соответствуют требованиям."
                                                     " Исполнение команды отменено.", reply_to_message_id=message_id)
            self.func_args = []

            if presend:
                return False

            # Если у хукера пустой список аргументов, его "сотрет" считыватель,
            # поэтому его обнуление равносильно удалению хукера.

    @classmethod
    def get_hooker(cls, user):

        # Если нет активного хукера у данного пользователя
        if str(user) not in cls.hookers.keys():
            return None

        hooker = cls.hookers[str(user)]

        # Если аргументы хукера уже считаны - выход
        if len(hooker.func_args) == 0:
            cls.hookers.pop(str(user))
            return None

        return hooker
