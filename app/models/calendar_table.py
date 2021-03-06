from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey,DateTime



class CalendarModel(db.Model):

    __tablename__ = 'calendar'


    id = db.Column(db.Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'))
    professional_id = Column(Integer, ForeignKey('professional.id', ondelete='CASCADE'))
    schedule = Column(DateTime, nullable=False)






