from enum import unique
from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Float
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class ProfessionalModel(db.Model):

    name: str
    gender: str
    age: int
    specialization: str
    description: str
    crm: str
    final_rating: float
    email: str
    contact: str

    __tablename__ = 'professional'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    gender = Column(String(1), nullable=False)
    age = Column(Integer, nullable=False)
    specialization = Column(String(32), nullable=False)
    description = Column(String(132), nullable=False)
    crm = Column(String(15), nullable=False)
    final_rating = Column(Float)
    email = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(50), nullable=False)
    contact = Column(String(50))

    @property
    def password(self):
        raise AttributeError('Password is not acessible.')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
