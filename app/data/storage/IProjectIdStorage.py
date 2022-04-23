from abc import ABC, abstractmethod

from app.data.storage import ProjectId


class IProjectIdStorage(ABC):
    """
    Interface
    ----------
    The interface used to save the project id in storage

    Methods
    -------
    save(project_id: ProjectId)
        Saving to Storage
    get()
        Getting the project id
    """

    @abstractmethod
    def save(self, project_id: ProjectId) -> bool:
        pass

    @abstractmethod
    def get(self) -> ProjectId:
        pass
