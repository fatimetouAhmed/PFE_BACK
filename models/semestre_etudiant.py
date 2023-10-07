from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
Base = declarative_base()
semestre_etudiants = Table(
    'semestre_etudiants',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('id_etu', Integer, ForeignKey('etudiants.id')),
    Column('id_sem', Integer, ForeignKey('semestres.id'))
)

class Etudiants(Base):
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
    semestres = relationship('Semestres', secondary=semestre_etudiants, backref='etudiants')

class Semestres(Base):
    __tablename__ = 'semestres'
    id = Column(Integer, primary_key=True)
    nom = Column(String(250))
    id_fil = Column(Integer,ForeignKey('filiere.id'))
    date_debut=Column(DateTime)
    date_fin=Column(DateTime)
    semestres_etudiants = relationship('Etudiants', secondary=semestre_etudiants, backref='semestres_etudiants')
