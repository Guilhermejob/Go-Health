from sqlalchemy.orm import relationship
from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String


@dataclass
class DeficiencyModel(db.Model):

    name: str

    __tablename__ = 'deficiencies'

    deficiency_id = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=False)

    clients = relationship(
        "ClientModel",
        secondary='deficiency_client',
        backref="deficiencies"
    )
