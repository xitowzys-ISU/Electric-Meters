from config import localization
from telegram import ReplyKeyboardMarkup, KeyboardButton

buttons = {
    'back': localization.getText("bot_back_button"),
}

defaultMenuButton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons['back'])
        ]
    ],
    resize_keyboard=True
)
