from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from loguru import logger as log

from app.telegramBot.handlers import TolokoSettingsHandler, mainHandler


SELECT_MENU = chr(0)

convTolokoSettingsHandler = ConversationHandler(
    entry_points=[MessageHandler(
        filters=Filters.text, callback=TolokoSettingsHandler.messageHandler)],

    states={
    },

    fallbacks=[],
    map_to_parent={
        SELECT_MENU: SELECT_MENU
    }
)

convMainHandler = ConversationHandler(
    entry_points=[
        CommandHandler(
            "start", mainHandler.mainHandler)],

    states={
        "NAME_PRODUCT": [convTolokoSettingsHandler],
        SELECT_MENU: [MessageHandler(
            filters=Filters.text, callback=mainHandler.messageHandler)],
    },

    fallbacks=[],
    allow_reentry=True
)
