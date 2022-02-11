from loguru import logger

from config import TELEGRAM_BOT_TOKEN
from config import localization

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, ForceReply
import telegram


def logger_configuration() -> None:

    # TODO: Добавить создание папки logs если её нету

    logger.add("./logs/logs.log", format="({time}) {level} {message}",
               level="DEBUG", rotation="10 KB", compression="zip", serialize=True)

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

        dispatcher.add_handler(CommandHandler("start", start))

        # logging.basicConfig(level=logging.DEBUG,
        #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        updater.start_polling()
        logger.success(localization.getText("bot_activate"))

        updater.idle()
    except telegram.error.Unauthorized:
        logger.error(localization.getText("bot_unauthorized"))
        exit(1)


def bootstrap() -> None:
    """Launching the application

    """

    start_bot(TELEGRAM_BOT_TOKEN)