from ast import Add
from telegram import Update
from telegram.ext import CallbackContext

from loguru import logger as log
from app.telegramBot.utils import HandlersContainer

from config import localization
from app.telegramBot.keyboards import AddExistProjectKeyboards

handlerContainer = HandlersContainer()


def messageHandler(update: Update, context: CallbackContext):
    text = update.message.text

    if (localization.getText("bot_back_button") == text):
        log.debug("back_button")
        handlerContainer["CreateProjectHandler"]["CreateProjectHandler"](
            update, context)
        return "BACK"
    else:
        pass


def AddExistProjectHandler(update: Update, context: CallbackContext):
    log.debug("Добавление существующего проекта")

    update.message.reply_text(
        text=localization.getText(
            "bot_handler_add_exist_project_get_link_text"),
        reply_markup=AddExistProjectKeyboards.defaultMenuButton
    )
