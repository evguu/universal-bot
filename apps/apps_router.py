import functools
from utils import permissions

handlers = {}
help_list = []


def command_route(commands, args=(), help_text="Описание команды.",
                  permission_required=("Basic",)):
    def wrapper(func):
        for command in commands:
            handlers[command] = (func, args, permission_required)
        help_list.append(
            (
                ", ".join(commands),
                permission_required,
                help_text
            )
        )

        @functools.wraps(func)
        def wrapped_func(*a, **kwa):
            return func(*a, **kwa)

        return wrapped_func

    return wrapper


def execute_app(command, **kwa):
    command = command.lower()

    # Проверяем существование введенной команды
    if command not in handlers:
        return False

    # Проверяем наличие у пользователя прав на использование этой команды
    if not permissions.has_permission(kwa["req"].user.perm_group, handlers[command][2]):
        kwa["server"].send_message(kwa["req"].user, "Нет прав на выполнение команды!")
        return True

    # Забираем только запрошенные обработчиком аргументы
    res_args = {}
    for key in handlers[command][1]:
        res_args[key] = kwa[key]

    # Вызываем обработчик с запрошенными им аргументами
    handlers[command][0](**res_args)
    return True
