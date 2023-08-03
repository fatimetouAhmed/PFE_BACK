from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

departementssuperviseurs = Table(
    'departementssuperviseurs',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('id_sup', Integer, ForeignKey('superviseurs.user_id'),primary_key=True),
    Column('id_dep', Integer, ForeignKey('departements.id'),primary_key=True),
    Column('date', DateTime,primary_key=True),
)

class Superviseur(Base):
    __tablename__ = "superviseurs"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True) 
    departements = relationship('Departements', secondary=departementssuperviseurs, backref='departements')

class Departements(Base):
    __tablename__ = 'departements'

    id = Column(Integer, primary_key=True)
    nom = Column(String(250))
    superviseurs = relationship('Superviseur', secondary=departementssuperviseurs, backref='superviseurs')
