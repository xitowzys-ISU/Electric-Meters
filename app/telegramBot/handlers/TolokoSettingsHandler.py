# from app.handlers.mainHandler import mainHandlerss
from telegram import Update
from telegram.ext import CallbackContext

from loguru import logger as log

from config import localization
from app.telegramBot.handlers import mainHandler, ProjectSettingsHandler
from app.telegramBot.keyboards import TolokoSettingsKeyboards


def messageHandler(update: Update, context: CallbackContext):
    text = update.message.text

    if (localization.getText("bot_back_button") == text):
        log.debug("back_button")
        mainHandler.mainHandler(update, context)
        return "BACK"
    elif (localization.getText("bot_keyboard_toloko_settings_project_setup") == text):
        log.debug("Проект")
        return ProjectSettingsHandler.ProjectSettingsHandler(update, context)
    elif (localization.getText("bot_main_back_button") == text):
        mainHandler.mainHandler(update, context)
        return "BACK_MENU"


def TolokoSettingsHandler(update: Update, context: CallbackContext):
    log.debug("Активирован найстройки Toloko")

    update.message.reply_text(
        text=localization.getText("bot_handler_tokolo_settings_welcome_text"),
        reply_markup=TolokoSettingsKeyboards.defaultMenuButton
    )

    return "NAME_PRODUCT"
