import functools

handlers = {}
autogenerated_help_message = "! Бот игнорирует регистр в командах.\n\n" \
                             "Список доступных вам команд:\n\n"


def get_autogenerated_help_message():
    return autogenerated_help_message


def command_route(commands, args=(), help_text="Описание команды."):

    def wrapper(func):
        global autogenerated_help_message
        for command in commands:
            handlers[command] = (func, args)

        autogenerated_help_message += ", ".join(commands) + ":\n" + help_text + "\n\n"

        @functools.wraps(func)
        def wrapped_func(*a, **kwa):
            return func(*a, **kwa)
        return wrapped_func

    return wrapper


def execute_app(command, **kwa):
    command = command.lower()
    if command not in handlers:
        return False
    res_args = {}
    for key in handlers[command][1]:
        res_args[key] = kwa[key]
    handlers[command][0](**res_args)
    return True
