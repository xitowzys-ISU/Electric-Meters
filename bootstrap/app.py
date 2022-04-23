import telegram
from telegram.ext import Updater

import sys
from loguru import logger
from app.data.repository.IInitDBRepositoryImpl import IInitDBRepositoryImpl
from app.data.storage.database.DatabaseInitStorage import DatabaseInitStorage
from app.domain.repository.IInitDBRepository import IInitDBRepository
from app.domain.usecase.InitDBTablesUsecase import InitDBTableUsecase
from app.telegramBot.utils import HandlersContainer
import app.domain.usecase as dUsecase

from config import localization, TELEGRAM_BOT_TOKEN


def logger_configuration() -> None:

    # TODO: Добавить создание папки logs если её нету

    # logger.add("./logs/logs.log", format="({time}) {level} {message}",
    #            level="DEBUG", rotation="10 KB", compression="zip", serialize=True)

    logger.remove()

    logger.add(
        sys.stdout, colorize=True, format="(<level>{level}</level>) [<green>{time:HH:mm:ss}</green>] ➤ <level>{message}</level>")


def init_database() -> None:
    project_id_repository: IInitDBRepository = IInitDBRepositoryImpl(
        DatabaseInitStorage())

    init_database: InitDBTableUsecase = dUsecase.InitDBTableUsecase(
        project_id_repository)

    init_database.execute()


def start_bot(token: str) -> None:

    from app.telegramBot.handlers.dispatchers.ConversationHandlers import convMainHandler

    try:

        updater = Updater(token)

        dispatcher = updater.dispatcher

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

    init_database()

    handlerContainer = HandlersContainer("app/telegramBot/handlers")

    start_bot(TELEGRAM_BOT_TOKEN)
