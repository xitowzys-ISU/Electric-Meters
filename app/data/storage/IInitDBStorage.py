from abc import ABC, abstractmethod

from app.data.storage import ProjectId


class IInitDBStorage(ABC):
    """
    Interface
    ----------
    The interface used for database initialization in storage

    Methods
    -------
    init() : bool
        Initialize database
    """

    @abstractmethod
    def init(self) -> bool:
        pass
