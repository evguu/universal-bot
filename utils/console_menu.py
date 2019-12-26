class _MenuItem:

    def __init__(self, text=None, submenu=None, function=None, function_args=None, _isback=False):
        if submenu and not _isback:
            self.text = submenu.name
        elif _isback:
            self.text = "Назад в " + submenu.name
        else:
            self.text = text
        self.submenu = submenu
        self.function = function
        self.function_args = function_args
        self._isback = _isback

    def exec(self):
        if self.submenu:
            Menu.get_active_menu().on_deactivate(**({"_out": True} if self._isback else {"_out": False}))
            self.submenu.activate(**({"_in": False} if self._isback else {"_in": True}))
        if self.function:
            if self.function_args:
                self.function(*self.function_args)
            else:
                self.function()


class Menu:
    stack = []

    @staticmethod
    def get_active_menu():
        return Menu.stack[-1]

    @staticmethod
    def get_previous_menu():
        return Menu.stack[-2]

    def press_item(self, num):
        try:
            self[int(num)].exec()
        except (IndexError, ValueError):
            print("Нет такого пункта!")

    def __init__(self, name):
        self.items = []
        self.name = name
        self.is_main = False

    def print(self):
        res = self.get_str_elements()
        res = "\n" + " > ".join([str(i) for i in Menu.stack]) + "\n" + res + "\nВвод: "
        print(res)

    def get_str_elements(self):
        res = []
        for i, item in enumerate(self.items):
            res.append("{}. {}".format(i, item.text))
        return "\n".join(res)

    def __repr__(self):
        return self.name

    def add_item(self, text=None, submenu=None, function=None, function_args=None, _isback=False):
        item = _MenuItem(text=text,
                         submenu=submenu,
                         function=function,
                         function_args=function_args,
                         _isback=_isback)
        self.items.append(item)

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)

    def activate(self, _in=True):
        if _in:
            Menu.stack.append(self)
        if not self.is_main:
            self.add_item(submenu=Menu.get_previous_menu(), _isback=True)

    def set_main(self):
        self.is_main = True
        self.activate()

    def on_deactivate(self, _out=False):
        if _out:
            Menu.stack.pop()
        if not self.is_main:
            self.pop_last_item()

    def pop_last_item(self):
        self.items.pop()
