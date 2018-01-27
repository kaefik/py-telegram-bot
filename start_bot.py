from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
import logging



class iTelegramBot:
    def __init__(self, token=None,level_loggining=logging.INFO):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=level_loggining)
        self.bot = Updater(token)
        self.bot.dispatcher.add_handler(CallbackQueryHandler(self.button))
        self.reg_handler("start",self.start)
        self.reg_handler("about",self.about)

    def reg_handler(self, command=None,hand=None):
        """ регистрация команд которые обрабатывает бот """
        if (command is None) or (hand is None):
            return
        self.bot.dispatcher.add_handler(CommandHandler(command, hand))
        

    def about(self, bot, update):
        """ сообщает какие есть возможности у бота """
        update.message.reply_text("Здесь перечислены, то что я умею.")

    def start(self, bot, update):       
        keyboard = [[InlineKeyboardButton("Help", callback_data="/about"),
                 InlineKeyboardButton("Settings", callback_data='/settings')],
                [InlineKeyboardButton("Option 3", callback_data='3')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Hello {}! I\'m glad to see you! '.format(update.message.from_user.first_name), reply_markup=reply_markup)
        

    def button(self, bot, update):
        query = update.callback_query
        bot.edit_message_text(text="{}".format(query.data),
                                chat_id=query.message.chat_id,
                                message_id=query.message.message_id) 
        # bot.send_message(chat_id=update.message.chat_id, text="{}".format(query.data))
          
    def run(self):
        """ запуск бота """   
        logging.debug("Start telegram bot")     
        self.bot.start_polling()
        self.bot.idle()


cfg = Config("config.ini")
tgbot = iTelegramBot(cfg.token,logging.DEBUG)
tgbot.run()