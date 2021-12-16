from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey


surgeryclientmodel = db.Table('surgery_client',

                              Column('client_id', Integer,
                                     ForeignKey('clients.id', ondelete='CASCADE')),
                              Column('surgery_id', Integer, ForeignKey(
                                     'surgeries.surgery_id'))

                              )
