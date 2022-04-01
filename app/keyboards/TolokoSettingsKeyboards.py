from config import localization
from telegram import ReplyKeyboardMarkup, KeyboardButton

buttons = {
    'project_setup': localization.getText("bot_keyboard_toloko_settings_project_setup"),
    'pool_setup': localization.getText("bot_keyboard_toloko_settings_pool_setup"),
    'current_setup': localization.getText("bot_keyboard_toloko_settings_current_setup"),
    'back': localization.getText("bot_back_button"),
    'back_menu': localization.getText("bot_main_back_button")
}

defaultMenuButton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons['current_setup'])
        ],
        [
            KeyboardButton(text=buttons['project_setup']),
            KeyboardButton(text=buttons['pool_setup'])

        ],
        [
            KeyboardButton(text=buttons['back']),
            KeyboardButton(text=buttons['back_menu'])

        ]
    ],
    resize_keyboard=True
)
