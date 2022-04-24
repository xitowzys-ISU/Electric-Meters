import re
from app.data.storage.models.ProjectId import ProjectId

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

        regex = r"^(?:http|https):\/\/([A-Z0-9\/]*(?:\.[A-Z0-9][A-Z0-9_-]*)+\/(?:[A-Z\/]*))([0-9]*)"

        result = re.search(regex, url.url, flags=re.I)

        if result:
            if result.group(1) == "toloka.yandex.ru/requester/project/":
                try:
                    int(result.group(2))
                    self.project_id_repository.save_project_id(
                        ProjectId(id=result.group(2)))
                except ValueError:
                    return False
            else:
                return False
        else:
            return False

        # self.project_id_repository.save_project_id(url)

        # print(self.project_id_repository.save_project_id(url))

        return True
