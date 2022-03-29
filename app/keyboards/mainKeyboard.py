from config import localization
from telegram import ReplyKeyboardMarkup, KeyboardButton

buttons = {
    'setup_YT': localization.getText("bot_keyboard_main_setting_up_yandex_toloko"),
    'collection_control': localization.getText("bot_keyboard_main_collection_control"),
    'link_docs': localization.getText("bot_keyboard_main_link_docs"),
    'storage_control': localization.getText("bot_keyboard_main_storage_control"),
}

defaultMenuButton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons['setup_YT']),
            KeyboardButton(text=buttons['collection_control'])
        ],
        [
            KeyboardButton(text=buttons['storage_control']),
            KeyboardButton(text=buttons['link_docs']),
        ]
    ],
    resize_keyboard=True
)
