from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey


diseaseclientmodel = db.Table('disease_client',

                              Column('client_id', Integer,
                                     ForeignKey('clients.client_id')),
                              Column('disease_id', Integer, ForeignKey(
                                     'diseases.disease_id'))

                              )
