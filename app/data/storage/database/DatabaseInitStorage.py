
import sqlalchemy as sa
from sqlalchemy import inspect
from loguru import logger as log
from app.data.storage.IInitDBStorage import IInitDBStorage
from app.data.storage.database.SQLAlchemy.declarative_base import Base
from app.data.storage.database.SQLAlchemy.engine import engine


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

    def init(self) -> bool:
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
