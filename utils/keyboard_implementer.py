class KeyboardCondition:

    def __init__(self):
        self.options = None
        self.is_keyboard_visible = False  # Используется для корректного закрытия клавиатуры у пользователя.


class KeyboardImplementer:
    """
    Класс для серверов, способных на отображение клиенту клавиатуры.
    """

    def __init__(self):
        self.users_keyboards = {}

    def options_to_buttons(self, user):
        """
        Метод, преобразующий options в валидные кнопки выбранного сервера.

        Переопределите, если формат кнопок у вашего сервера не соответствует стандартному.
        Стандартный формат: [["B1"], ["B2"]]
        Метод должен ИЗМЕНЯТЬ, а не возвращать.
        """
        pass

    def form_request(self, user, message, reply_to_message_id=None):
        """
        Метод, формирующий запрос для отправки на сервер в соответствии с установленной клавиатурой.
        """
        raise NotImplementedError

    def set_options(self, user, options):
        if repr(user) not in self.users_keyboards:
            self.users_keyboards[repr(user)] = KeyboardCondition()
        self.users_keyboards[repr(user)].is_keyboard_visible = True
        self.users_keyboards[repr(user)].options = options
        if options:
            self.users_keyboards[repr(user)].options.append(["--Отмена--"])
        self.options_to_buttons(user)
