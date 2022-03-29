from config import localization
from telegram import Update
from telegram.ext import CallbackContext

from app.keyboards import mainKeyboard


def mainHandler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=localization.getText("bot_handler_main_text"),
        reply_markup=mainKeyboard.defaultMenuButton
    )
