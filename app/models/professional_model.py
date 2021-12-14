from sqlalchemy.orm import relationship
from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Float
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class ProfessionalModel(db.Model):
    id: int
    name: str
    last_name: str
    specialization: str
    final_rating: float
    email: str
    phone: str
    crm: str

    __tablename__ = 'professional'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(String(1), nullable=False)
    age = Column(Integer, nullable=False)
    specialization = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)
    crm = Column(String(15), nullable=False, unique=True)
    final_rating = Column(Float)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    phone = Column(String(15))

    rating = relationship("ProfessionalRatingModel", backref="professional")

    @property
    def password(self):
        raise AttributeError('Password is not acessible.')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

    def serialize(self):
        return {
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "description": self.description,
            "specialization": self.specialization,
            "CRM": self.crm,
            "final_rating": self.final_rating,
            "email": self.email,
            "phone": self.phone,
        }
