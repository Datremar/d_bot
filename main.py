from itertools import chain
from src.games.tiktaktoe import Table, Player, AI, Game

import telebot

bot = telebot.TeleBot('1843675124:AAG13lQZ7tLE_nA2Td-QJdCDoOvKQyWFzLc')
game = None
table = None


def set_player1(message):
    print('Setting player1')
    global game

    sign = message.text
    game.player1 = Player(sign)

    send = bot.send_message(message.chat.id, 'Выбери уровень компьютера:')
    bot.register_next_step_handler(send, set_player2)


def set_player2(message):
    print('Setting player2')
    global game

    ai_sign = 'X' if game.player1.sign == 'O' else 'O'

    lvl = message.text
    game.player2 = AI(ai_sign, int(lvl))

    bot.send_message(message.chat.id, table.__str__())
    send = bot.send_message(message.chat.id, 'Введи координаты ячейки:')
    bot.register_next_step_handler(send, receive_cords)


def receive_cords(message):
    print('Receiving coords')
    global game

    x, y = map(int, message.text.split())

    game.set_move(x, y)

    bot.register_next_step_handler(message, player1_move)


def player1_move(message):
    print('Player 1 move')
    global game
    global table

    game.player1.make_move(*game.get_move(), table=table)
    game.move()

    bot.register_next_step_handler(message.chat.id, make_move)


def player2_move(message):
    print('Player 2 move')
    global game
    global table

    game.player2.do_the_thing(table)
    game.move()

    bot.register_next_step_handler(message.chat.id, make_move)


def make_move(message):
    print('Applying move')
    global game
    global table

    bot.send_message(message.chat.id, table.__str__())

    send = None

    is_over, who_won = is_game_over(table)
    if is_over:
        if who_won != 'DRAW':
            bot.send_message(message.chat.id, f'Победил: {who_won}')
        else:
            bot.send_message(message.chat.id, 'Ничья :Р')

        return

    if game.x_turn:
        if game.player1.sign == 'X':
            send = bot.send_message(message.chat.id, 'Введите координаты ячейки:')
            bot.register_next_step_handler(send, receive_cords)

        elif game.player2.sign == 'X':
            bot.register_next_step_handler(message.chat.id, player2_move)

    else:
        if game.player1.sign == 'O':
            send = bot.send_message(message.chat.id, 'Введите координаты ячейки:')
            bot.register_next_step_handler(send, receive_cords)

        elif game.player2.sign == 'O':
            bot.register_next_step_handler(message.chat.id, player2_move)


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


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Hello!")


@bot.message_handler(commands=['appointment'])
def make_appointment(message):
    timetable = [str((time, time % 2 == 0)) for time in range(10)]
    bot.send_message(message.chat.id, '\n'.join(timetable))


@bot.message_handler(commands=['tik-tak-toe'])
def tik_tak_toe(message):
    bot.send_message(message.chat.id, "Начнем!")

    global table
    global game

    table = Table()
    game = Game()

    send = bot.send_message(message.chat.id, 'Выбери свой значок: ')
    bot.register_next_step_handler(send, set_player1)


if __name__ == '__main__':
    bot.polling()
