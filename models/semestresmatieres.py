from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

semestresmatieres = Table(
    'semestresmatieres',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('id_mat', Integer, ForeignKey('matieres.id'),primary_key=True),
    Column('id_sem', Integer, ForeignKey('semestres.id'),primary_key=True),
)

class Semestres(Base):
    __tablename__ = 'semestres'
    id = Column(Integer, primary_key=True)
    nom = Column(String(250))
    id_fil = Column(Integer,ForeignKey('filiere.id'))
    date_debut=Column(DateTime)
    date_fin=Column(DateTime)
    matieres = relationship('Matiere', secondary=semestresmatieres, backref='matieres')

class Matiere(Base):
    __tablename__ = 'matieres'

    id = Column(Integer, primary_key=True)
    libelle = Column(String(250))
    nbre_heure = Column(Integer)
    credit = Column(Integer)
    filieres = relationship('Semestres', secondary=semestresmatieres, backref='semestres')
