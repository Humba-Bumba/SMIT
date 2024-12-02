from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql

Base = declarative_base()


class Rate(Base):
    __tablename__ = "rates"
    uuid: UUID = Column(postgresql.UUID(as_uuid=True), default=uuid4, nullable=False, primary_key=True)
    cargo_type = Column(String, index=True)
    rate = Column(Float, nullable=False)
    effective_date = Column(DateTime, default=datetime.now())
