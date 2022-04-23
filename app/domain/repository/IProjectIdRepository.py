from abc import ABC, abstractmethod

from app.domain.models import ProjectId


class IProjectIdRepository(ABC):
    """
    Interface
    ----------
    The interface used to save the project id

    Methods
    -------
    save_project_id(project_id: Project_id)
        Saving project id
    get()
        Getting the project id
    """

    @abstractmethod
    def save_project_id(self, project_id: ProjectId) -> bool:
        pass

    @abstractmethod
    def get_project_id(self) -> ProjectId:
        pass
