from app.telegramBot.utils import HandlersContainer
from config import localization
from telegram import Update
from telegram.ext import CallbackContext

from loguru import logger as log

from app.telegramBot.keyboards import PoolsSettingsKeyboards

handlerContainer = HandlersContainer()


def messageHandler(update: Update, context: CallbackContext):
    text = update.message.text
    log.debug("messageHandler")

    if (localization.getText("bot_back_button") == text):
        log.debug("back_button")
        handlerContainer["TolokoSettingsHandler"]["TolokoSettingsHandler"](
            update, context)
        return "BACK"

    elif (localization.getText("bot_keyboard_pools_settings_create_pools") == text):
        handlerContainer["CreatePoolsHandler"]["CreatePoolsHandler"](
            update, context)
        return "CREATE_POOLS"

    elif (localization.getText("bot_main_back_button") == text):
        handlerContainer["mainHandler"]["mainHandler"](update, context)
        return "BACK_MENU"


def PoolsSettingsHandler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=localization.getText("bot_handler_pools_settings_welcome_text"),
        reply_markup=PoolsSettingsKeyboards.defaultMenuButton
    )

    log.debug("ok")
