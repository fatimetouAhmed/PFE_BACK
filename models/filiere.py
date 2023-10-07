from sqlalchemy import Table,Column,String,Integer,ForeignKey
from config.db import meta
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
Base = declarative_base()
class Filieres(Base):
    __tablename__ = 'filieres'

    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    description = Column(String(255))
    id_dep = Column(Integer, ForeignKey('departements.id'))

    departements = relationship("Departements", primaryjoin="Filieres.id_dep == Departements.id")
    departements = relationship("Departements")
    
class Departements(Base):
    __tablename__ = 'departements'

    id = Column(Integer, primary_key=True)
    nom = Column(String(255))

    