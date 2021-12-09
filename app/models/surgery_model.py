from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, ForeignKey


@dataclass
class SurgeryModel(db.Model):

    name: str

    __tablename__ = 'surgeries'

    surgery_id = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.client_id'))
