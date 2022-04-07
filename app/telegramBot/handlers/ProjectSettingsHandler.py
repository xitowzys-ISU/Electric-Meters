from config import localization
from telegram import Update
from telegram.ext import CallbackContext

from loguru import logger as log

from app.telegramBot.keyboards import ProjectSettingsKeyboards
from . import mainHandler, TolokoSettingsHandler


def messageHandler(update: Update, context: CallbackContext):
    text = update.message.text
    log.debug("messageHandler")

    if (localization.getText("bot_back_button") == text):
        log.debug("back_button")
        TolokoSettingsHandler.TolokoSettingsHandler(update, context)
        return "BACK"
    elif (localization.getText("bot_main_back_button") == text):
        mainHandler.mainHandler(update, context)
        return "BACK_MENU"


def ProjectSettingsHandler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=localization.getText("bot_handler_main_text"),
        reply_markup=ProjectSettingsKeyboards.defaultMenuButton
    )

    log.debug("ok")

    return "PROJECT_SETTINGS"
