from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from app.telegramBot.utils import HandlersContainer

handlerContainer = HandlersContainer()


convAddExistProjectHandler = ConversationHandler(
    entry_points=[MessageHandler(
        filters=Filters.text, callback=handlerContainer["AddExistProjectHandler"]["messageHandler"])],

    states={
    },

    fallbacks=[],
    map_to_parent={
        "BACK": "SHOW_CREATE_PROJECT_KEYBOARD"
    }
)

convCreateProjectHandler = ConversationHandler(
    entry_points=[MessageHandler(
        filters=Filters.text, callback=handlerContainer["CreateProjectHandler"]["messageHandler"])],

    states={
        "SHOW_CREATE_PROJECT_KEYBOARD": [MessageHandler(
            filters=Filters.text, callback=handlerContainer["CreateProjectHandler"]["messageHandler"])],
        "ADD_EXIST_PROJECT": [convAddExistProjectHandler]
    },

    fallbacks=[],
    map_to_parent={
        "BACK": "SHOW_PROJECT_SETTINGS_KEYBOARD",
        "BACK_MENU": "BACK_MENU"
    }
)

convProjectSettingsHandler = ConversationHandler(
    entry_points=[MessageHandler(
        filters=Filters.text, callback=handlerContainer["ProjectSettingsHandler"]["messageHandler"])],

    states={
        "SHOW_PROJECT_SETTINGS_KEYBOARD": [MessageHandler(
            filters=Filters.text, callback=handlerContainer["ProjectSettingsHandler"]["messageHandler"])],
        "CREATE_PROJECT": [convCreateProjectHandler]
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
