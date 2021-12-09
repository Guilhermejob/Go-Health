from app.configs.database import db
from sqlalchemy.orm import relationship

from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, ForeignKey


@dataclass
class DiseaseModel(db.Model):

    name: str

    __tablename__ = 'diseases'

    disease_id = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=False)

    clients = relationship(
        "ClientModel",
        secondary='disease_client',
        backref="diseases"
    )
