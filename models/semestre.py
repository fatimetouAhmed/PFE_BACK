from sqlalchemy import Table,Column,String,Integer,DateTime,ForeignKey
from config.db import meta
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Semestre(Base):
    __tablename__ = 'semestres'

    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    id_fil = Column(Integer, ForeignKey('filieres.id'))
    date_debut=Column(DateTime)
    date_fin=Column(DateTime)
    filieres = relationship("Filieres", primaryjoin="Semestre.id_fil == Filieres.id")
    filieres = relationship("Filieres")
    
class Filieres(Base):
    __tablename__ = 'filieres'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    description = Column(String(255))
