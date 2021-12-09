from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class ClientModel(db.Model):

    name: str
    last_name: str
    age: str
    email: str
    gender: str
    height: int
    weigth: float
    imc: str

    __tablename__ = 'clients'

    client_id = Column(Integer, primary_key=True)
    name = Column(String(63), nullable=False)
    last_name = Column(String(63), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    gender = Column(String(63), nullable=False)
    height = Column(Float, nullable=False)
    weigth = Column(Float, nullable=False)
    imc = Column(Float, nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not acessible.')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
