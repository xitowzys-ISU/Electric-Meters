from loguru import logger as log
from app.data.storage import IProjectIdStorage
from app.data.storage.models.ProjectId import ProjectId

import sqlalchemy as sa
from app.data.storage.database.SQLAlchemy.declarative_base import Base
from app.data.storage.database.SQLAlchemy.engine import engine
from sqlalchemy.orm.exc import NoResultFound


class DatabaseProjectIdStorage(IProjectIdStorage):
    """
    Class
    ----------
    The class used to save and get the project id to the database

    Implemented interfaces
    ----------
    IProjectIdStorage

    Methods
    -------
    save(project_id: ProjectId)
        Saving project id
    get()
        Getting the project id
    """

    def save(self, project_id: ProjectId) -> bool:

        from app.data.storage.database.models.TolokoSettings import TolokoSettings

        Session = sa.orm.sessionmaker()
        Session.configure(bind=engine)
        session = Session()

        try:
            toloko_settings = session.query(TolokoSettings).one()

            toloko_settings.project_id = project_id.id

            session.commit()

            log.success(f"Изменен ID проекта: {project_id.id}")
        except NoResultFound as e:
            new_toloko_settings = TolokoSettings(project_id=project_id.id)
            session.add(new_toloko_settings)
            session.commit()

            log.success(f"Добавлен новый ID проекта: {project_id.id}")

        return True

    def get(self) -> ProjectId:
        pass
