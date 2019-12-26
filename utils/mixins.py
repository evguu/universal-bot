from utils.exceptions import NoMessageIdToReplyException


class KeyboardCondition:

    def __init__(self):
        self.options = None
        self.is_keyboard_visible = False  # Используется для корректного закрытия клавиатуры у пользователя.


class KeyboardMixin:
    """
    Примесь для поддержки клавиатуры сервером.

    Любой наследник этого класса должен иметь атрибут reply_to_message_id.
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

    def set_options(self, user, options):
        if repr(user) not in self.users_keyboards:
            self.users_keyboards[repr(user)] = KeyboardCondition()
        self.users_keyboards[repr(user)].is_keyboard_visible = True
        self.users_keyboards[repr(user)].options = options
        if options:
            self.users_keyboards[repr(user)].options.append(["--Отмена--"])
        self.options_to_buttons(user)
