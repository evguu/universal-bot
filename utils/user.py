class User:
    def __init__(self, server, user_id, dialog_id):
        self.server = server
        self.user_id = user_id
        self.dialog_id = dialog_id

    def __repr__(self):
        return "User({}, {}, {})".format(self.server, self.user_id, self.dialog_id)

    def __str__(self):
        return "{}@{}:{}".format(self.server, self.user_id, self.dialog_id)
