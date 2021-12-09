from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class FoodPlanModel(db.Model):

    pdf: str
    start_time: str
    expiration: str

    __tablename__ = 'food_plan'

    id = Column(Integer, primary_key=True)
    pdf = Column(String, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow())
    expiration = Column(
        DateTime, default=datetime.utcnow() + timedelta(days=90))
    client_id = Column(Integer, ForeignKey(
        'clients.client_id'), nullable=False)
    professional_id = Column(Integer, nullable=False)
