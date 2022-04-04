from config import localization
from telegram import Update
from telegram.ext import CallbackContext

from app.telegramBot.keyboards import mainKeyboard
from . import TolokoSettingsHandler


def messageHandler(update: Update, context: CallbackContext):
    text = update.message.text

    if (text == localization.getText("bot_keyboard_main_setting_up_yandex_toloko")):

        return TolokoSettingsHandler.TolokoSettingsHandler(update, context)


def mainHandler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=localization.getText("bot_handler_main_text"),
        reply_markup=mainKeyboard.defaultMenuButton
    )
    return "SHOW_MAIN_KEYBOARD"
