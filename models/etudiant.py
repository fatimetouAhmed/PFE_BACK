from sqlalchemy import Column, String, Integer,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
    date_insecription = Column(DateTime)
