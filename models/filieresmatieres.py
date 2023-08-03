from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

filieresmatieres = Table(
    'filieresmatieres',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('id_mat', Integer, ForeignKey('matieres.id'),primary_key=True),
    Column('id_fil', Integer, ForeignKey('filieres.id'),primary_key=True),
)

class Filieres(Base):
    __tablename__ = 'filieres'

    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    description = Column(String(255))
    matieres = relationship('Matiere', secondary=filieresmatieres, backref='matieres')

class Matiere(Base):
    __tablename__ = 'matieres'

    id = Column(Integer, primary_key=True)
    libelle = Column(String(250))
    nbre_heure = Column(Integer)
    credit = Column(Integer)
    filieres = relationship('Filieres', secondary=filieresmatieres, backref='filieres ')
