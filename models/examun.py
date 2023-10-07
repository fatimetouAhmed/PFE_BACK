from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
Base = declarative_base()


examuns = Table(
    'examuns',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('type', String(250)),
    Column('heure_deb', DateTime),
    Column('heure_fin', DateTime),
    Column('id_mat', Integer, ForeignKey('matieres.id'), primary_key=True),
    Column('id_sal', Integer, ForeignKey('salles.id'), primary_key=True),
)

class Salle(Base):
    __tablename__ = 'salles'

    id = Column(Integer, primary_key=True)
    nom = Column(String(250))

    matieres = relationship('Matieres', secondary=examuns, backref='salles')

class Matieres(Base):
    __tablename__ = 'matieres'

    id = Column(Integer, primary_key=True)
    libelle = Column(String(250))
    nbre_heure = Column(Integer)
    credit = Column(Integer)
    matieres_salles = relationship('Salle', secondary=examuns, backref='matieres_salles')
