from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from loguru import logger as log

from app.telegramBot.handlers import TolokoSettingsHandler, mainHandler

convProjectSettingsHandler = ConversationHandler(
    entry_points=[MessageHandler(
        filters=Filters.text, callback=TolokoSettingsHandler.messageHandler)],

    states={
    },

    fallbacks=[],
    map_to_parent={
        "SHOW_MAIN_KEYBOARD": "SHOW_MAIN_KEYBOARD"
    }
)

convTolokoSettingsHandler = ConversationHandler(
    entry_points=[MessageHandler(
        filters=Filters.text, callback=TolokoSettingsHandler.messageHandler)],

    states={
    },

    fallbacks=[],
    map_to_parent={
        "SHOW_MAIN_KEYBOARD": "SHOW_MAIN_KEYBOARD"
    }
)

convMainHandler = ConversationHandler(
    entry_points=[
        CommandHandler(
            "start", mainHandler.mainHandler)],

    states={
        "NAME_PRODUCT": [convTolokoSettingsHandler],
        "SHOW_MAIN_KEYBOARD": [MessageHandler(
            filters=Filters.text, callback=mainHandler.messageHandler)],
    },

    fallbacks=[],
    allow_reentry=True
)
