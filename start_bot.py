from telegram.ext import Updater, CommandHandler
from config import Config


class iTelegramBot:
    def __init__(self, token=None):
        self.bot = Updater(token)
        self.reg_handler("hello",self.hello)

    def reg_handler(self, command=None,hand=None):
        """ регистрация команд которые обрабатывает бот """
        if (command is None) or (hand is None):
            return
        self.bot.dispatcher.add_handler(CommandHandler('hello', self.hello))

    def hello(self, bot, update):
        update.message.reply_text(
            'Hello {}'.format(update.message.from_user.first_name))

    def run(self):
        """ запуск бота """
        self.bot.start_polling()
        self.bot.idle()


cfg = Config("config.ini")
tgbot = iTelegramBot(cfg.token)
tgbot.run()