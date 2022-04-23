import re

from app.domain.models.ProjectUrl import ProjectUrl
from app.domain.repository.IProjectIdRepository import IProjectIdRepository


class SaveProjectIdUsecase():
    """
    Class
    ----------
    The usecase used to save the project id

    Parameters
    ----------
    project_id_repository : IProjectIdRepository
        Interface for saving the project id

    Methods
    -------
    execute(url: ProjectUrl)
        Execute usecase
    """

    def __init__(self, project_id_repository: IProjectIdRepository):
        self.project_id_repository: IProjectIdRepository = project_id_repository
        pass

    def execute(self, url: ProjectUrl) -> bool:

        # self.project_id_repository.save_project_id(url)

        print(self.project_id_repository.save_project_id(url))

        return True
