import sqlalchemy as sa
from app.data.storage.database.SQLAlchemy.declarative_base import Base
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from dataclasses import dataclass


@dataclass
class ProjectsId(Base):
    __tablename__ = 'projects_id'

    id = sa.Column(INTEGER(unsigned=True),
                   primary_key=True, autoincrement=True)
    project_id = sa.Column(INTEGER(unsigned=True), nullable=True)

    pools_id = relationship("PoolsId", backref="projects_id")
    toloko_settings = relationship("TolokoSettings", backref="projects_id")
