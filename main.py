from src.app.app import app
from src.bot import bot


class Main:
    def __init__(self):
        self.bot = bot
        self.app = app

    def main(self):
        self.bot.polling()


if __name__ == '__main__':
    Main().main()
