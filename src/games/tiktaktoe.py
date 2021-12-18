from itertools import chain
from random import choice


class Table:
    EMPTY_CELL = ' '
    moves = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    def __init__(self):
        self.table = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]

    def check(self, x: int, y: int, sign: str):
        if not self.occupied(x, y):
            self.table[x][y] = sign

            return 'OK'
        else:
            print('Эта ячейка тебе не рада :x')

            return 'ERROR'

    def occupied(self, x: int, y: int):
        return self.table[x][y] != ' '

    def get_sign(self, x, y):
        return self.table[x][y]

    def get_table(self):
        return self.table

    def copy_table(self, table: list):
        for i in range(3):
            for j in range(3):
                self.table[i][j] = table[i][j]

    def __str__(self):
        view = ''

        for line in self.table:
            line = list(map(lambda x: '_' if x == ' ' else x, line))
            tmp = ' '.join(line) + '\n'

            view += tmp

        return view


class Player:
    def __init__(self, sign: str):
        self.sign = sign

    def make_move(self, x: int, y: int, table: Table):
        table.check(x, y, self.sign)


class AI(Player):
    def __init__(self, sign: str, level: int):
        super().__init__(sign)
        self.level = level

    def lvl1_move(self, table: Table):
        free_cells = []

        for x in range(3):
            for y in range(3):
                if not table.occupied(x, y):
                    free_cells.append((x, y))

        cell = choice(free_cells)

        self.make_move(*cell, table=table)

    def i_win_here(self, cells: list, table: Table):
        move = None
        line = []
        for cell in cells:
            if not table.occupied(*cell):
                move = cell
            line.append(table.get_sign(*cell))

        return line.count(self.sign) == 2 and line.count(Table.EMPTY_CELL), move

    def i_lose_here(self, cells: list, table: Table):
        move = None
        line = []
        for cell in cells:
            if not table.occupied(*cell):
                move = cell
            line.append(table.get_sign(*cell))

        enemy_sign = 'X' if self.sign == 'O' else 'O'

        return line.count(enemy_sign) == 2 and line.count(Table.EMPTY_CELL), move

    def lvl2_move(self, table: Table):
        moves = Table.moves

        for line in moves:
            do_i_win, move = self.i_win_here(line, table)

            if do_i_win:
                self.make_move(*move, table=table)
                return None

        for line in moves:
            do_i_lose, move = self.i_lose_here(line, table)

            if do_i_lose:
                self.make_move(*move, table=table)
                return None

        self.lvl1_move(table)

    def do_the_thing(self, table: Table):
        if self.level == 1:
            self.lvl1_move(table)
        elif self.level == 2:
            self.lvl2_move(table)


def is_game_over(table: Table):
    moves = Table.moves

    for move in moves:
        line = [table.get_sign(*cell) for cell in move]

        if line.count('X') == 3:
            return True, 'X'

        if line.count('O') == 3:
            return True, 'O'

    if all(table.get_sign(*cell) != ' ' for line in list(chain(moves)) for cell in line):
        return True, 'DRAW'

    return False, None


class Game:
    def __init__(self):
        self.p_sign = ''
        self.ai_sign = ''
        self.ai_lvl = 0
        self.x = -1
        self.y = -1
        self.x_turn = True

    def set_player_sign(self, sign):
        self.p_sign = sign

    def set_ai_sign(self, sign):
        self.ai_sign = sign

    def set_ai_level(self, level):
        self.ai_lvl = level

    def set_move(self, x, y):
        self.x = x
        self.y = y

    def get_move(self):
        return self.x, self.y

    def move(self):
        self.x_turn = not self.x_turn


if __name__ == '__main__':
    table = Table()

    p_sign = input('Выберите значок: ')

    player1 = Player(p_sign)

    ai_sign = 'X' if p_sign == 'O' else 'O'
    ai_lvl = int(input('Выберите уровень компьютера:\n  1 - легкий; 2 - средний;\n 3 - хардкор;\n'))

    player2 = AI(ai_sign, ai_lvl)

    running = True
    x_turn = True

    while running:
        print(table)

        is_over, who_won = is_game_over(table)
        if is_over:
            if who_won != 'DRAW':
                print(f'Победил: {who_won}')
            else:
                print('Ничья :Р')

            break

        if x_turn:
            if player1.sign == 'X':
                print('Введи координаты ячейки: ')

                x, y = int(input()), int(input())
                player1.make_move(x, y, table)
            elif player2.sign == 'X':
                player2.do_the_thing(table)
        else:
            if player1.sign == 'O':
                print('Введи координаты ячейки: ')

                x, y = int(input()), int(input())
                player1.make_move(x, y, table)
            elif player2.sign == 'O':
                player2.do_the_thing(table)

        x_turn = not x_turn
