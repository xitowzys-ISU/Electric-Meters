from app.data.storage.IInitDBStorage import IInitDBStorage
from app.domain.repository.IInitDBRepository import IInitDBRepository


class IInitDBRepositoryImpl(IInitDBRepository):
    """
    Class
    ----------
    Repository implementation used to initialize database

    Implemented interfaces
    ----------
    IInitDBRepository

    Parameters
    ----------
    init_db_storage : IInitDBStorage
        Interface for initializing the database in the repository
    """

    def __init__(self, init_db_storage: IInitDBStorage):
        self.init_db_storage: IInitDBStorage = init_db_storage

    def init_tables(self) -> bool:
        return self.init_db_storage.init()
