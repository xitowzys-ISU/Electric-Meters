import sqlalchemy as sa
from app.data.storage.database.SQLAlchemy.declarative_base import Base
from sqlalchemy.dialects.mysql import INTEGER

from dataclasses import dataclass


@dataclass
class TolokoSettings(Base):
    __tablename__ = 'toloka_settings'

    id = sa.Column(INTEGER(unsigned=True),
                   primary_key=True, autoincrement=True)
    name = sa.Column(sa.VARCHAR(length=255), nullable=True)
    project_id = sa.Column(INTEGER(unsigned=True), nullable=True)
    collection_pool_id = sa.Column(
        INTEGER(unsigned=True), nullable=True)
    verification_pool_id = sa.Column(
        INTEGER(unsigned=True), nullable=True)
