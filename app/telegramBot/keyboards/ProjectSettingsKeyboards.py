from config import localization
from telegram import ReplyKeyboardMarkup, KeyboardButton

buttons = {
    'create_project': localization.getText("bot_keyboard_project_settings_create_project"),
    'delete_project': localization.getText("bot_keyboard_project_settings_delete_project"),
    'edit_project': localization.getText("bot_keyboard_project_settings_edit_project"),
    'back': localization.getText("bot_back_button"),
    'back_menu': localization.getText("bot_main_back_button")
}

defaultMenuButton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons['create_project'])
        ],
        [
            KeyboardButton(text=buttons['edit_project']),
            KeyboardButton(text=buttons['delete_project'])

        ],
        [
            KeyboardButton(text=buttons['back']),
            KeyboardButton(text=buttons['back_menu'])

        ]
    ],
    resize_keyboard=True
)
