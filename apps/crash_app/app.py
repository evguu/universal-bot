from apps.apps_router import command_route
from utils.exceptions import TestException


@command_route(commands=["/crash"],
               help_text="Вызывает искусственное исключение для отладки.",
               permission_required=["Owner"])
def _():
    raise TestException("Проверочное исключение.")
