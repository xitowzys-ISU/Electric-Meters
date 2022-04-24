from config import localization
from telegram import ReplyKeyboardMarkup, KeyboardButton

buttons = {
    'pool_new': localization.getText("bot_keyboard_create_pools_new"),
    'pool_template': localization.getText("bot_keyboard_create_pools_template"),
    'pool_add_existing': localization.getText("bot_keyboard_create_pools_add_existing"),
    'back': localization.getText("bot_back_button"),
    'back_menu': localization.getText("bot_main_back_button")
}

defaultMenuButton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons['pool_new'])
        ],
        [
            KeyboardButton(text=buttons['pool_template']),
            KeyboardButton(text=buttons['pool_add_existing'])

        ],
        [
            KeyboardButton(text=buttons['back']),
            KeyboardButton(text=buttons['back_menu'])

        ]
    ],
    resize_keyboard=True
)
