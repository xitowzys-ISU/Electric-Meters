from app.telegramBot.utils import HandlersContainer
from config import localization
from telegram import Update
from telegram.ext import CallbackContext

from loguru import logger as log

from app.telegramBot.keyboards import CreatePoolsKeyboards

handlerContainer = HandlersContainer()


def messageHandler(update: Update, context: CallbackContext):
    text = update.message.text
    log.debug("messageHandler")

    if (localization.getText("bot_back_button") == text):
        log.debug("back_button")
        handlerContainer["PoolsSettingsHandler"]["PoolsSettingsHandler"](
            update, context)
        return "BACK"

    elif (localization.getText("bot_keyboard_create_pools_new") == text):
        update.message.reply_text(
            text=localization.getText(
                "bot_lack_functionality_message")
        )

    elif (localization.getText("bot_keyboard_create_pools_template") == text):
        update.message.reply_text(
            text=localization.getText(
                "bot_lack_functionality_message")
        )

    elif (localization.getText("bot_keyboard_create_pools_add_existing") == text):
        handlerContainer["AddExistProjectHandler"]["AddExistProjectHandler"](
            update, context)
        return "ADD_EXIST_POOLS"

    elif (localization.getText("bot_main_back_button") == text):
        handlerContainer["mainHandler"]["mainHandler"](update, context)
        return "BACK_MENU"


def CreatePoolsHandler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=localization.getText("bot_handler_pools_settings_welcome_text"),
        reply_markup=CreatePoolsKeyboards.defaultMenuButton
    )

    log.debug(localization.getText(
        "bot_debug_log_create_pools_welcome_text"))
