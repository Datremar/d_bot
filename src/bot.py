import telebot

bot = telebot.TeleBot('1843675124:AAG13lQZ7tLE_nA2Td-QJdCDoOvKQyWFzLc')


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Hello!")


@bot.message_handler(commands=['appointment'])
def make_appointment(message):
    timetable = [str((time, time % 2 == 0)) for time in range(10)]
    bot.send_message(message.chat.id, '\n'.join(timetable))
