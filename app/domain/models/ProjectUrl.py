from dataclasses import dataclass


@dataclass
class ProjectUrl:
    """
    Dataclass
    ----------
    The data class used to store the project url

    Attributes
    ----------
    id : int
        project id
    """
    url: str
