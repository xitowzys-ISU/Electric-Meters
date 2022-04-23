from loguru import logger as log
from app.domain.repository.IInitDBRepository import IInitDBRepository


class InitDBTableUsecase():
    """
    Class
    ----------
    The usecase used to initialize tables in the database

    Parameters
    ----------
    init_db_repository : IInitDBRepository
        Interface for database initialization

    Methods
    -------
    execute()
        Execute usecase
    """

    def __init__(self, init_db_repository: IInitDBRepository):
        self.init_db_repository: IInitDBRepository = init_db_repository
        pass

    def execute(self) -> bool:
        log.info("Инициализация таблиц в базу данных")
        return self.init_db_repository.init_tables()
