from apps.apps_router import command_route
from database import database
from utils import permissions
from utils.hooker_decorator import multipart_input
from utils.hookers import HookerArgData
from utils.user import User


@command_route(commands=["/give_right"],
               args=["req", "args"],
               help_text="Добавить право пользователю.",
               permission_required=["Owner"])
def _(req, args):
    @multipart_input(req, args,
                     HookerArgData(lambda x: "@" in x,
                                   "Введите server_user_id пользователя."),
                     HookerArgData(permissions.is_valid_right_name,
                                   "Введите право.",
                                   greedy=True))
    def _(suid, right):
        if suid == "@":
            suid = req.user.server_user_id

        # Если заданный пользователь существует, но не загружен, загружаем его.
        if suid not in User.user_data_from_db:
            User(*suid.split("@"), 0)

        permissions.add_right(User.user_data_from_db[suid][0], right)
        database.update_permission_record(User.user_data_from_db[suid][0], suid)
        return "Право выдано."


@command_route(commands=["/remove_right"],
               args=["req", "args"],
               help_text="Забрать у пользователя право.",
               permission_required=["Owner"])
def _(req, args):
    @multipart_input(req, args,
                     HookerArgData(lambda x: "@" in x,
                                   "Введите server_user_id пользователя."),
                     HookerArgData(lambda x: True,
                                   "Введите право."))
    def _(suid, right):
        if suid == "@":
            suid = req.user.server_user_id

        # Если заданный пользователь существует, но не загружен, загружаем его.
        if suid not in User.user_data_from_db:
            User(*suid.split("@"), 0)

        permissions.remove_right(User.user_data_from_db[suid][0], right)
        database.update_permission_record(User.user_data_from_db[suid][0], suid)
        return "Право отобрано, если оно вообще было."


@command_route(commands=["/status"],
               args=["server", "req"],
               help_text="Узнать свой статус.",
               permission_required=[])
def _(server, req):
    server.send_message(req.user, "Ваш идентификатор прав:\n{}".format(permissions.str_perm(req.user.perm_group)))
