from app.data.storage import IProjectIdStorage
from app.domain.models import ProjectId as DomainModelProjectId
from app.data.storage.models.ProjectId import ProjectId as StorageModelProjectId
from app.domain.repository.IProjectIdRepository import IProjectIdRepository


class ProjectIdRepositoryImpl(IProjectIdRepository):
    """
    Class
    ----------
    Repository implementation used to save the project ID

    Implemented interfaces
    ----------
    IProjectIdRepository

    Parameters
    ----------
    i_project_id_storage : IProjectIdStorage
        Interface for saving the project ID to the storage
    """

    def __init__(self, i_project_id_storage: IProjectIdStorage):
        self.i_project_id_storage: IProjectIdStorage = i_project_id_storage

    def save_project_id(self, dm_project_id: DomainModelProjectId) -> bool:
        sm_project_id: StorageModelProjectId = StorageModelProjectId(
            id=dm_project_id.id)

        result = self.i_project_id_storage.save(sm_project_id)

        return result

    def get_project_id(self) -> DomainModelProjectId:
        pass
