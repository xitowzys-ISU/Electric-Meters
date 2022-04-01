from .HandlersContainer import HandlersContainer
from config import localization
from telegram import Update
from telegram.ext import CallbackContext

from app.keyboards import mainKeyboard


def mainHandler(update: Update, context: CallbackContext):
    handlersContainer = HandlersContainer()
    handlersContainer.disableAllHandler()
    handlersContainer.enableHandler("mainHandler")
    handlersContainer.enableHandler("messageHandler")

    update.message.reply_text(
        text=localization.getText("bot_handler_main_text"),
        reply_markup=mainKeyboard.defaultMenuButton
    )
