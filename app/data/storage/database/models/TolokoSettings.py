import sqlalchemy as sa
from app.data.storage.database.SQLAlchemy.declarative_base import Base
from app.data.storage.database.models.ProjectsId import ProjectsId
from sqlalchemy.dialects.mysql import INTEGER

from dataclasses import dataclass


@dataclass
class TolokoSettings(Base):
    __tablename__ = 'toloka_settings'

    id = sa.Column(INTEGER(unsigned=True),
                   primary_key=True, autoincrement=True)
    name = sa.Column(sa.VARCHAR(length=255), nullable=True)
    project_id = sa.Column(INTEGER(unsigned=True),
                           sa.ForeignKey(ProjectsId.id), nullable=False)
