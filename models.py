from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, UniqueConstraint, CheckConstraint
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional
class Base(DeclarativeBase):
    pass

class Meteodata(Base):
    __tablename__ = 'meteodata'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    temperature: Mapped[int]
    pressure: Mapped[int]
    humidity: Mapped[int]
    created: Mapped[datetime]

    __table_args__=(
        (UniqueConstraint('created', name='unique_creation_time')),
    )

