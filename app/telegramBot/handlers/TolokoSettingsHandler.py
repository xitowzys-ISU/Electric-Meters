from telegram import Update
from telegram.ext import CallbackContext

from loguru import logger as log
from app.telegramBot.utils import HandlersContainer

from config import localization
from app.telegramBot.keyboards import TolokoSettingsKeyboards

handlerContainer = HandlersContainer()


def messageHandler(update: Update, context: CallbackContext):
    text = update.message.text

    if (localization.getText("bot_back_button") == text):
        log.debug("back_button")
        handlerContainer["mainHandler"]["mainHandler"](update, context)
        return "BACK"

    elif (localization.getText("bot_keyboard_toloko_settings_project_setup") == text):
        log.debug("Проект")
        handlerContainer["ProjectSettingsHandler"]["ProjectSettingsHandler"](
            update, context)
        return "PROJECT_SETTINGS"

    elif (localization.getText("bot_keyboard_toloko_settings_pool_setup") == text):
        log.debug("Пул")
        handlerContainer["PoolsSettingsHandler"]["PoolsSettingsHandler"](
            update, context)
        return "POOLS_SETTINGS"

    elif (localization.getText("bot_main_back_button") == text):
        handlerContainer["mainHandler"]["mainHandler"](update, context)
        return "BACK_MENU"


def TolokoSettingsHandler(update: Update, context: CallbackContext):
    log.debug("Активирован найстройки Toloko")

    update.message.reply_text(
        text=localization.getText("bot_handler_tokolo_settings_welcome_text"),
        reply_markup=TolokoSettingsKeyboards.defaultMenuButton
    )

    return "NAME_PRODUCT"
