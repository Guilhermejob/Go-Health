from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

from app.exceptions.client_exceptions import UnauthorizedError
from app.exceptions.schedules_exceptions import ProfessionalNotFoundError


@dataclass
class ClientModel(db.Model):
    id: int
    name: str
    last_name: str
    email: str

    __tablename__ = 'clients'

    mandatory_keys = ["name", "last_name", "age",
                      "email", "password", "gender", "height", "weigth"]
    optional_keys = ["diseases", "surgeries",
                     "deficiencies"]

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    gender = Column(String(1), nullable=False)
    height = Column(Float, nullable=False)
    weigth = Column(Float, nullable=False)
    imc = Column(Float, nullable=False)

    food_plan = relationship(
        "FoodPlanModel", backref=backref("client", uselist=False))

    schedules = relationship(
        "ProfessionalModel",
        secondary='calendar',
        backref="schedules",
        uselist=True
    )

    @property
    def password(self):
        raise AttributeError('Password is not acessible.')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

    def check_professional(self, professional_id):
        if not self.schedules:
            raise UnauthorizedError(
                'You not have any appointment whith this client')
        if professional_id != self.schedules[-1].id:
            raise UnauthorizedError(
                'You do not have anymore appointment whith this client')

    def serialize(self):
        professional = self.schedules
        if professional:
            professional = self.schedules[-1]

        return {
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "gender": self.gender,
            "height": self.height,
            "weigth": self.weigth,
            "imc": self.imc,
            "diseases": [{"name": disease.name} for disease in self.diseases],
            "surgeries": [{"name": surgery.name} for surgery in self.surgeries],
            "deficiencies": [{"name": deficiency.name} for deficiency in self.deficiencies],
            "professional": self.schedules,
            "food_plan": [plan for plan in self.food_plan]
        }
