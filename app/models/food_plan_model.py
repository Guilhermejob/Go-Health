from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class FoodPlanModel(db.Model):

    id: int
    pdf_name: str
    start_time: str
    expiration: str

    __tablename__ = 'food_plan'

    id = Column(Integer, primary_key=True)
    pdf_name = Column(String)
    pdf = Column(LargeBinary)
    start_time = Column(DateTime, default=datetime.utcnow())
    expiration = Column(
        DateTime, default=datetime.utcnow() + timedelta(days=90))
    client_id = Column(Integer, ForeignKey(
        'clients.id', ondelete='CASCADE'))
    professional_id = Column(Integer, nullable=False)
