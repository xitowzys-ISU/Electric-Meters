import sqlalchemy as sa
from app.data.storage.database.SQLAlchemy.declarative_base import Base
from app.data.storage.database.models.PoolsId import PoolsId
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL

from dataclasses import dataclass


@dataclass
class VerifyingResponse(Base):
    __tablename__ = 'verifying_responses'

    id = sa.Column(INTEGER(unsigned=True),
                   primary_key=True, autoincrement=True)
    pool_id = sa.Column(INTEGER(unsigned=True),
                        sa.ForeignKey(PoolsId.id), nullable=True)
    requirement_true_answers = sa.Column(DECIMAL(10, 1), nullable=True)
    public_comment = sa.Column(sa.VARCHAR(length=255), nullable=True)
