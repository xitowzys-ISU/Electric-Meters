import enum
import sqlalchemy as sa
from app.data.storage.database.SQLAlchemy.declarative_base import Base
from app.data.storage.database.models.ProjectsId import ProjectsId
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from dataclasses import dataclass


class TypeEnum(enum.Enum):
    verification = "VERIFICATION"
    collecting = "COLLECTING"


@dataclass
class PoolsId(Base):
    __tablename__ = 'pools_id'

    id = sa.Column(INTEGER(unsigned=True),
                   primary_key=True, autoincrement=True)
    project_id = sa.Column(INTEGER(unsigned=True),
                           sa.ForeignKey(ProjectsId.id))
    pool_id = sa.Column(INTEGER(unsigned=True), nullable=True)
    type = sa.Column(sa.Enum(TypeEnum), nullable=True)
