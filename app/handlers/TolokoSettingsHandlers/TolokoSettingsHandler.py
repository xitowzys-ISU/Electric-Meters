from config import localization
from telegram import Update
from loguru import logger as log
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, CommandHandler, Filters
from app.keyboards import TolokoSettingsKeyboards
from ..HandlersContainer import HandlersContainer


def test(update: Update, context: CallbackContext):
    text = update.message.text

    log.debug("Проект")
    if (text == localization.getText("bot_keyboard_toloko_settings_project_setup")):
        log.debug("Проект")


def TolokoSettingsHandler(update: Update, context: CallbackContext):

    handlersContainer = HandlersContainer()
    print(handlersContainer)

    log.debug("Активирован найстройки Toloko")

    update.message.reply_text(
        text=localization.getText("bot_handler_main_text"),
        reply_markup=TolokoSettingsKeyboards.defaultMenuButton
    )

    convHandler = ConversationHandler(
        entry_points=[MessageHandler(
            filters=Filters.text, callback=messageHandler)],

        states={
            # "NAME_PRODUCT": [MessageHandler(Filters.text, searchProductHandler.searchProductHandler)],
        },

        fallbacks=[CommandHandler('stop', None)]
    )

    handlersContainer.addHandler(convHandler, "TolokoConvHandler")
    handlersContainer.disableHandler("messageHandler")

    text = update.message.text
    # update.message.reply_text(
    #     text=localization.getText("bot_handler_main_text"),
    #     reply_markup=mainKeyboard.defaultMenuButton
    # )


def messageHandler(update: Update, context: CallbackContext):
    text = update.message.text
    if (text == localization.getText("bot_keyboard_toloko_settings_project_setup")):
        log.debug("Проект")
