from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

etudiermats = Table(
    'etudiermats',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('id_etu', Integer, ForeignKey('etudiants.id')),
    Column('id_mat', Integer, ForeignKey('matieres.id'))
)

class Etudiant(Base):
    __tablename__ = 'etudiants'

    id = Column(Integer, primary_key=True)
    nom = Column(String(250))
    prenom = Column(String(250))
    photo = Column(String(250))
    genre = Column(String(250))
    date_N = Column(DateTime)
    lieu_n = Column(String(250))
    email = Column(String(250))
    telephone = Column(String(250))
    nationalite = Column(String(250))
    date_insecription = Column(DateTime)  # Correction du nom de colonne
    matieres = relationship('Matiere', secondary=etudiermats, backref='etudiants')

class Matiere(Base):
    __tablename__ = 'matieres'

    id = Column(Integer, primary_key=True)
    libelle = Column(String(250))
    nbre_heure = Column(Integer)
    credit = Column(Integer)
    matieres_etudiants = relationship('Etudiant', secondary=etudiermats, backref='matieres_etudiants')
