from telegram import Update
from telegram.ext import CallbackContext

from loguru import logger as log
from app.data.repository import ProjectIdRepositoryImpl
from app.data.storage.database.DatabaseProjectIdStorage import DatabaseProjectIdStorage
from app.domain.models.ProjectUrl import ProjectUrl
from app.domain.repository.IProjectIdRepository import IProjectIdRepository
from app.domain.usecase.SaveProjectIdUsecase import SaveProjectIdUsecase
from app.telegramBot.utils import HandlersContainer

from config import localization
from app.telegramBot.keyboards import AddExistProjectKeyboards

import app.domain.models as dModels
import app.domain.usecase as dUsecase

handlerContainer = HandlersContainer()


def messageHandler(update: Update, context: CallbackContext):
    text = update.message.text

    if (localization.getText("bot_back_button") == text):
        log.debug("back_button")
        handlerContainer["CreateProjectHandler"]["CreateProjectHandler"](
            update, context)
        return "BACK"
    else:
        url: ProjectUrl = dModels.ProjectUrl(url=text)

        project_id_repository: IProjectIdRepository = ProjectIdRepositoryImpl(
            DatabaseProjectIdStorage())

        save_project_id: SaveProjectIdUsecase = dUsecase.SaveProjectIdUsecase(
            project_id_repository)

        if save_project_id.execute(url):
            update.message.reply_text(text="ID проекта изменен")
        else:
            update.message.reply_text(text="Неккоректный url")


def AddExistProjectHandler(update: Update, context: CallbackContext):
    log.debug("Добавление существующего проекта")

    update.message.reply_text(
        text=localization.getText(
            "bot_handler_add_exist_project_get_link_text"),
        reply_markup=AddExistProjectKeyboards.defaultMenuButton
    )
