from abc import ABC, abstractmethod

from app.domain.models import ProjectId


class IInitDBRepository(ABC):
    """
    Interface
    ----------
    The interface used for database initialization

    Methods
    -------
    init_tables()
        Initialize tables
    """

    @abstractmethod
    def init_tables(self) -> bool:
        pass
