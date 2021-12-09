from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, ForeignKey


@dataclass
class ProfessionalRatingModel(db.Model):

    rating: int

    __tablename__ = 'professional_rating'

    id = Column(Integer, primary_key=True)
    professional_id = Column(Integer, nullable=False)
    rating = Column(Integer)
    client_id = Column(Integer, nullable=False)