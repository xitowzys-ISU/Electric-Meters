from app.data.storage import IProjectIdStorage
from app.data.storage.models.ProjectId import ProjectId


class DatabaseProjectIdStorage(IProjectIdStorage):
    """
    Class
    ----------
    The class used to save and get the project id to the database

    Implemented interfaces
    ----------
    IProjectIdStorage

    Methods
    -------
    save(project_id: ProjectId)
        Saving project id
    get()
        Getting the project id
    """

    def save(self, project_id: ProjectId) -> bool:
        return f"СОХРАНЕНИЕ В БАЗУ ДАННЫЙ ID {project_id}"

    def get(self) -> ProjectId:
        pass
