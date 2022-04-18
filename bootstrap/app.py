import telegram
from telegram.ext import Updater

import sys
from loguru import logger
from app.telegramBot.utils import HandlersContainer

from config import localization, TELEGRAM_BOT_TOKEN


def logger_configuration() -> None:

    # TODO: Добавить создание папки logs если её нету

    # logger.add("./logs/logs.log", format="({time}) {level} {message}",
    #            level="DEBUG", rotation="10 KB", compression="zip", serialize=True)

    logger.remove()

    logger.add(
        sys.stdout, colorize=True, format="(<level>{level}</level>) [<green>{time:HH:mm:ss}</green>] ➤ <level>{message}</level>")


logger_configuration()


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def start_bot(token: str) -> None:

    try:

        updater = Updater(token)

        dispatcher = updater.dispatcher

        from app.telegramBot.handlers.dispatchers.ConversationHandlers import convMainHandler

        dispatcher.add_handler(convMainHandler)

        updater.start_polling()
        logger.success(localization.getText("bot_logger_activate"))

        updater.idle()
    except telegram.error.Unauthorized:
        logger.error(localization.getText("bot_logger_unauthorized"))
        exit(1)


def bootstrap() -> None:
    """Launching the application

    """
    logger_configuration()

    handlerContainer = HandlersContainer("app/telegramBot/handlers")

    start_bot(TELEGRAM_BOT_TOKEN)
