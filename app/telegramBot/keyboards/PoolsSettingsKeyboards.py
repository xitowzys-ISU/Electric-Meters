from config import localization
from telegram import ReplyKeyboardMarkup, KeyboardButton

buttons = {
    'create_pools': localization.getText("bot_keyboard_pools_settings_create_pools"),
    'delete_pools': localization.getText("bot_keyboard_pools_settings_delete_pools"),
    'edit_pools': localization.getText("bot_keyboard_pools_settings_edit_pools"),
    'back': localization.getText("bot_back_button"),
    'back_menu': localization.getText("bot_main_back_button")
}

defaultMenuButton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons['create_pools'])
        ],
        [
            KeyboardButton(text=buttons['edit_pools']),
            KeyboardButton(text=buttons['delete_pools'])

        ],
        [
            KeyboardButton(text=buttons['back']),
            KeyboardButton(text=buttons['back_menu'])

        ]
    ],
    resize_keyboard=True
)
