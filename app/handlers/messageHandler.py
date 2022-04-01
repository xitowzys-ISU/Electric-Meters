from config import localization
from telegram import Update
from loguru import logger as log
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler
from .TolokoSettingsHandlers import TolokoSettingsHandler


def messageHandler(update: Update, context: CallbackContext):
    text = update.message.text

    if (text == localization.getText("bot_keyboard_main_setting_up_yandex_toloko")):

        TolokoSettingsHandler(update, context)

    # if (text == localization.getText("bot_keyboard_toloko_settings_project_setup")):
    #     log.debug("Проект")

    # update.message.reply_text(
    #     text=localization.getText("bot_handler_main_text"),
    #     reply_markup=mainKeyboard.defaultMenuButton
    # )
