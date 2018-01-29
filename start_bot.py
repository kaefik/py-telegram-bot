from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
import logging

ABOUT = range(1)

class iTelegramBot:
    def __init__(self, token=None,level_loggining=logging.INFO):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=level_loggining)
        self.bot = Updater(token)
        """
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                "about":    [CallbackQueryHandler(self.about)]
                #"settings": [CallbackQueryHandler(self.second)]
            },
            fallbacks=[CommandHandler('start', self.start)]
        )
        self.bot.dispatcher.add_handler(self.conv_handler)
        """
        # обработка документов
        handlerDocument = MessageHandler(filters = Filters.document, callback=self.get_document)
        self.bot.dispatcher.add_handler(handlerDocument)

        # регистрация обработчика используя паттерн срабатывания
        self.bot.dispatcher.add_handler(CallbackQueryHandler(self.about2,pattern="^about_bot$")) 
        # регистрация обработчика для inline клавиатуры
        self.bot.dispatcher.add_handler(CallbackQueryHandler(self.inlinebutton))   
        # регистрация команд     
        self.reg_handler("start",self.start)
        self.reg_handler("about",self.about2)
        self.reg_handler("docs",self.docs)

    # обработка получение документов от пользователя (сохранение в указанной папке)
    def get_document(self,bot,update):
        file_id = update.message.document.file_id
        filename = update.message.document.file_name
        newFile = bot.get_file(file_id)
        newFile.download('files/savedoc/'+filename)

    def reg_handler(self, command=None,hand=None):
        """ регистрация команд которые обрабатывает бот """
        if (command is None) or (hand is None):
            return
        self.bot.dispatcher.add_handler(CommandHandler(command, hand))
        

    def about(self, bot, update):
        """ сообщает какие есть возможности у бота """
        update.message.reply_text("Здесь перечислены, то что я умею.")
    
    def about2(self, bot, update):
        """ сообщает какие есть возможности у бота """
        query = update.callback_query
        bot.send_message(text="Здесь перечислены, то что я умею.",chat_id=query.message.chat_id)

    def start(self, bot, update):       
        keyboard = [[InlineKeyboardButton("Help", callback_data="about_bot"),
                 InlineKeyboardButton("Settings", callback_data='settings')],
                [InlineKeyboardButton("Яndex", url='http://ya.ru')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Hello {}! I\'m glad to see you! '.format(update.message.from_user.first_name), reply_markup=reply_markup)
        

    def docs(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text = "Отправка файла...ждите...")
        bot.send_document(chat_id=update.message.chat_id, document=open('files/1.xlsx', 'rb'))
        

    def inlinebutton(self, bot, update):
        query = update.callback_query
        
        if format(query.data)=="about":
            pass
        else:
            bot.edit_message_text(text="{}".format(query.data),
                                chat_id=query.message.chat_id,
                                message_id=query.message.message_id) 
          
    def run(self):
        """ запуск бота """   
        logging.debug("Start telegram bot")  
        self.bot.start_polling()
        self.bot.idle()


cfg = Config("config.ini")
tgbot = iTelegramBot(cfg.token,logging.DEBUG)
tgbot.run()