from apps.apps_router import command_route, help_list
from utils import permissions

# Важно помнить, что бот игнорирует регистр в командах.
help_template = "Список доступных вам команд:\n\n"


def get_help_text(perm=()):
    result = help_template
    for item in help_list:
        # item имеет следующую структуру:
        # ("Алиасы команд через запятые и пробелы", ("Требуемые", "права"), "Описание команды.")
        if permissions.has_permission(perm, item[1]):
            result += ">> {} -> {}\n\n".format(item[0], item[2])
    return result


@command_route(commands=["/help"],
               args=["server", "req"],
               help_text="Узнать, какие команды умеет выполнять этот бот.",
               permission_required=[])
def _(server, req):
    server.send_message(req.user, get_help_text(req.user.perm_group))
