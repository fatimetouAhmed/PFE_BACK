from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
Base = declarative_base()


surveillances = Table(
    'surveillance',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('date_debut', DateTime),
    Column('date_fin', DateTime),
    Column('surveillant_id', Integer, ForeignKey('surveillants.user_id'), primary_key=True),
    Column('salle_id', Integer, ForeignKey('salles.id'), primary_key=True),
)

class Surveillants(Base):
    __tablename__ = 'surveillants'

    user_id = Column(Integer, primary_key=True)
    surveillances = relationship('Salles', secondary=surveillances, backref='surveillants')

class Salles(Base):
    __tablename__ = 'salles'
    id = Column(Integer, primary_key=True)
    nom = Column(String(250))
    surveillances_salles = relationship('Surveillants', secondary=surveillances, backref='surveillances_salles')
