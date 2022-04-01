# from app.handlers.mainHandler import mainHandlerss
from telegram import Update
from telegram.ext import CallbackContext

from loguru import logger as log

from config import localization
from app.telegramBot.handlers import mainHandler
from app.telegramBot.keyboards import TolokoSettingsKeyboards


def messageHandler(update: Update, context: CallbackContext):
    text = update.message.text

    if (localization.getText("bot_back_button") == text):
        log.debug("back_button")
        mainHandler.mainHandler(update, context)
        return chr(0)


def TolokoSettingsHandler(update: Update, context: CallbackContext):
    log.debug("Активирован найстройки Toloko")

    update.message.reply_text(
        text=localization.getText("bot_handler_main_text"),
        reply_markup=TolokoSettingsKeyboards.defaultMenuButton
    )

    return "NAME_PRODUCT"
