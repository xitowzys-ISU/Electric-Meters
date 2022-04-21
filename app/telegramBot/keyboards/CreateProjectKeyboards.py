from config import localization
from telegram import ReplyKeyboardMarkup, KeyboardButton

buttons = {
    'project_new': localization.getText("bot_keyboard_create_project_new"),
    'project_template': localization.getText("bot_keyboard_create_project_template"),
    'project_add_existing': localization.getText("bot_keyboard_create_project_add_existing"),
    'back': localization.getText("bot_back_button"),
    'back_menu': localization.getText("bot_main_back_button")
}

defaultMenuButton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons['project_new'])
        ],
        [
            KeyboardButton(text=buttons['project_template']),
            KeyboardButton(text=buttons['project_add_existing'])

        ],
        [
            KeyboardButton(text=buttons['back']),
            KeyboardButton(text=buttons['back_menu'])

        ]
    ],
    resize_keyboard=True
)
