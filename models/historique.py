from sqlalchemy import Table,Column,String,Integer,ForeignKey,DateTime,Boolean
from config.db import meta
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Historiques(Base):
    __tablename__ = 'historiques'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    id_exam = Column(Integer, ForeignKey('examuns.id'))
    examuns = relationship("Examuns", primaryjoin="Historiques.id_exam == Examuns.id")
    examuns = relationship("Examuns")
    
class Examuns(Base):
    __tablename__ = 'examuns'

    id = Column(Integer, primary_key=True)
    type = Column(String(255))
    heure_deb = Column(DateTime)
    heure_fin = Column(DateTime)
    id_mat = Column(String(255))
    id_mat= Column(String(255))

    