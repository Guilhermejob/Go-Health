from app.configs.database import db
from sqlalchemy.orm import relationship
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, ForeignKey


@dataclass
class SurgeryModel(db.Model):

    name: str

    __tablename__ = 'surgeries'

    surgery_id = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=False)

    clients = relationship(
        "ClientModel",
        secondary='surgery_client',
        backref="surgeries"
    )
