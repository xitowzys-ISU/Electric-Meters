from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from app.telegramBot.utils import HandlersContainer

handlerContainer = HandlersContainer()

convAddExistPoolHandler = ConversationHandler(
    entry_points=[MessageHandler(
        filters=Filters.text, callback=handlerContainer["AddExistPoolHandler"]["messageHandler"])],

    states={
    },

    fallbacks=[],
    map_to_parent={
        "BACK": "SHOW_CREATE_POOLS_KEYBOARD"
    }
)

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

convCreatePoolsHandler = ConversationHandler(
    entry_points=[MessageHandler(
        filters=Filters.text, callback=handlerContainer["CreatePoolsHandler"]["messageHandler"])],

    states={
        "SHOW_CREATE_POOLS_KEYBOARD": [MessageHandler(
            filters=Filters.text, callback=handlerContainer["CreatePoolsHandler"]["messageHandler"])],
        "ADD_EXIST_POOLS": [convAddExistPoolHandler]
    },

    fallbacks=[],
    map_to_parent={
        "BACK": "SHOW_POOLS_SETTINGS_KEYBOARD",
        "BACK_MENU": "BACK_MENU"
    }
)

convPoolsSettingsHandler = ConversationHandler(
    entry_points=[MessageHandler(
        filters=Filters.text, callback=handlerContainer["PoolsSettingsHandler"]["messageHandler"])],

    states={
        "SHOW_POOLS_SETTINGS_KEYBOARD": [MessageHandler(
            filters=Filters.text, callback=handlerContainer["PoolsSettingsHandler"]["messageHandler"])],
        "CREATE_POOLS": [convCreatePoolsHandler]
    },

    fallbacks=[],
    map_to_parent={
        "BACK": "SHOW_TOLOKO_SETTINGS_KEYBOARD",
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
        "POOLS_SETTINGS": [convPoolsSettingsHandler],
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
