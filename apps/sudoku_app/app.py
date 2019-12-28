from apps.apps_router import command_route
from utils.hookers import HookerArgData, Hooker
from utils.hooker_decorator import multipart_input


class Board:
    def __init__(self, tiles):
        """
        Создает доску судоку.
        """
        self.tiles = tiles

    def validate_tile_solution(self, tile_solution, pos):
        """
        Возвращает возможность поставить <tile_solution> на позицию <pos>.

        Число не может повторяться в строке, столбце или квадрате.
        """
        row, col = pos

        # Подтвердить строку
        for j in range(9):
            if self.tiles[row][j] == tile_solution and j != col:
                return False

        # Подтвердить столбец
        for i in range(9):
            if self.tiles[i][col] == tile_solution and i != row:
                return False

        # Подтвердить квадрат
        sq_row = row // 3  # Номер квадрата в столбце - его строка
        sq_col = col // 3  # Номер квадрата в строке - его столбец
        for i in range(sq_row * 3, sq_row * 3 + 3):
            for j in range(sq_col * 3, sq_col * 3 + 3):
                if self.tiles[i][j] == tile_solution and i != row and j != col:
                    return False

        # Если число не нарушило правила, оно может стоять в соответствующей клетке.
        return True

    def validate_solvability(self):
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j]:
                    if not self.validate_tile_solution(self.tiles[i][j], (i, j)):
                        return False
        return True

    def find_empty_tile(self):
        """
        Возвращает координаты первой найденной пустой клетки, либо None при отсутствии таковых.
        """
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j] == 0:
                    return i, j
        return None

    def get_printed_board(self):
        res = ""
        for i in range(9):
            if i % 3 == 0 and i != 0:
                res += "- " * 11 + "\n"
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    res += "| "
                res += (str(self.tiles[i][j]) if self.tiles[i][j] else "_") + " "
            res += "\n"
        return res

    def solve_board(self):
        """
        Рекурсивно решает доску используя backtracking.
        """
        if not self.validate_solvability():
            return False
        while 1:
            pos = self.find_empty_tile()

            # Если пустых клеток нет, то доска решена.
            if not pos:
                return True

            row, col = pos
            for attempt in range(1, 10):
                if self.validate_tile_solution(attempt, pos):
                    self.tiles[row][col] = attempt
                    if self.solve_board():
                        return True
                    self.tiles[row][col] = 0
            return False


@command_route(commands=["/solve"],
               args=["req", "args"],
               help_text="Решить судоку.")
def execute(req, args):

    def validate(x: str):
        cleaned = "".join([i for i in x if i in "0123456789"])
        if len(cleaned) < 9:
            return False
        return True

    @multipart_input(req, args, *[HookerArgData(validate, "[0 - неизвестно.] Строка " + str(i)) for i in range(1, 10)])
    def hooker_done(*rows):
        board = Board([[int(j) for j in i if j in "0123456789"][0:9]
                       for i in rows[0:9]])
        if board.solve_board():
            res = board.get_printed_board()
        else:
            res = "Нельзя решить!!!"
        return res
