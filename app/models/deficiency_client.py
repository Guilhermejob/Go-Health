from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey


deficiencyclientmodel = db.Table('deficiency_client',

                                 Column('client_id', Integer,
                                        ForeignKey('clients.id')),
                                 Column('deficiency_id', Integer, ForeignKey(
                                     'deficiencies.deficiency_id'))

                                 )
