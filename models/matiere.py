from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.etudiant import Etudiant
from models.etudiermat import etudiermats

Base = declarative_base()

class Matiere(Base):
    __tablename__ = 'matieres'

    id = Column(Integer, primary_key=True)
    libelle = Column(String(250))
    nbre_heure = Column(Integer)
    credit = Column(Integer)
    matieres_etudiants = relationship('Etudiant', secondary=etudiermats, backref='matieres_etudiants')
