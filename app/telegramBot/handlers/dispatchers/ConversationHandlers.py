from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from app.telegramBot.utils import HandlersContainer

handlerContainer = HandlersContainer()

convProjectSettingsHandler = ConversationHandler(
    entry_points=[MessageHandler(
        filters=Filters.text, callback=handlerContainer["ProjectSettingsHandler"]["messageHandler"])],

    states={
    },

    fallbacks=[],
    map_to_parent={
        "BACK": "SHOW_TOLOKO_SETTINGS_KEYBOARD",
        "BACK_MENU": "BACK_MENU"
    }
)

convTolokoSettingsHandler = ConversationHandler(
    entry_points=[MessageHandler(
        filters=Filters.text, callback=handlerContainer["TolokoSettingsHandler"]["messageHandler"])],

    states={
        "PROJECT_SETTINGS": [convProjectSettingsHandler],
        "SHOW_TOLOKO_SETTINGS_KEYBOARD": [MessageHandler(
            filters=Filters.text, callback=handlerContainer["TolokoSettingsHandler"]["messageHandler"])]
    },

    fallbacks=[],
    map_to_parent={
        "BACK": "SHOW_MAIN_KEYBOARD",
        "BACK_MENU": "SHOW_MAIN_KEYBOARD"
    }
)

convMainHandler = ConversationHandler(
    entry_points=[
        CommandHandler(
            "start", handlerContainer["mainHandler"]["mainHandler"])],

    states={
        "NAME_PRODUCT": [convTolokoSettingsHandler],
        "SHOW_MAIN_KEYBOARD": [MessageHandler(
            filters=Filters.text, callback=handlerContainer["mainHandler"]["messageHandler"])],
    },

    fallbacks=[],
    allow_reentry=True
)
