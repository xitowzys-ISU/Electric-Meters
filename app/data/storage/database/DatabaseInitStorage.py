
import sqlalchemy as sa
from sqlalchemy import inspect
from loguru import logger as log
from app.data.storage.IInitDBStorage import IInitDBStorage
from config import DB_USERNAME, DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT
from app.data.storage.database.SQLAlchemy.declarative_base import Base


class DatabaseInitStorage(IInitDBStorage):
    """
    Class
    ----------
    The class used to ...

    Implemented interfaces
    ----------
    IInitDBStorage

    Methods
    -------
    init() : bool
        ...
    """

    def __import_tables(self) -> None:
        import app.data.storage.database.models.TolokoSettings
        import app.data.storage.database.models.TestTable

    def init(self) -> bool:
        engine = sa.create_engine(
            f"mariadb+mariadbconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")

        self.__import_tables()

        log.info(f"Проверка таблиц")

        is_all_tables_exist = True

        for table in Base.metadata.tables.keys():
            if not sa.inspect(engine).has_table(table):
                is_all_tables_exist = False

                log.warning(f"Таблица {table} не существует")

                Base.metadata.create_all(
                    engine, tables=[Base.metadata.tables[table]])
                log.success(f"Таблица {table} создана")

        if is_all_tables_exist:
            log.success(f"Все таблицы уже проинициализированны")

        return True
