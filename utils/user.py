from database import database
from utils import permissions
import time


class User:
    # Структура:
    # suid:(stringified permission, ban timestamp or None, ban reason or None)
    user_data_from_db = {}

    def add_record(self):
        database.add_record(self.server_user_id, self.banned_until, self.banned_for, permissions.str_perm(self.perm_group))

    def __init__(self, server, user_id, dialog_id):
        """
        Так как пользователи в БД, нужно их оттуда загрузить либо создать для них запись.
        """
        self.server = server
        self.user_id = user_id
        self.dialog_id = dialog_id
        self.id = "{}@{}:{}".format(server, user_id, dialog_id)
        self.server_user_id = "{}@{}".format(server, user_id)
        if self.server_user_id in User.user_data_from_db:
            # Если пользователь уже загружен, используем эти данные.
            self.perm_group, self.banned_until, self.banned_for = User.user_data_from_db[self.server_user_id]
        else:
            user_record = database.get_record(self.server_user_id)
            if user_record:
                # Если пользователь существует в базе данных, загружаем оттуда.
                self.perm_group = permissions.destr_perm(user_record[3])
                self.banned_until = user_record[1]
                self.banned_for = user_record[2]
            else:
                # Если не существует, создаем базового пользователя.
                self.perm_group = permissions.permissionBasic
                self.banned_until = None
                self.banned_for = None
                self.add_record()
            User.user_data_from_db[self.server_user_id] = [
                self.perm_group,
                self.banned_until,
                self.banned_for
            ]

    def __repr__(self):
        return "User({}, {})".format(self.id, self.perm_group)
