from sqlalchemy import Table,Column,String,Integer
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Departements(Base):
    __tablename__ = 'departements'
    id = Column(Integer, primary_key=True)
    nom = Column(String(250))