from datetime import datetime
from sqlalchemy import Table,Column,String,Integer,ForeignKey,DateTime,Boolean,DATETIME
from config.db import meta
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Notifications(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    content = Column(String(255))
    date = Column(DATETIME,default=datetime.now)
    superviseur_id = Column(Integer, ForeignKey('superviseurs.user_id'))
    is_read = Column(Boolean)
    id_exam = Column(Integer, ForeignKey('examuns.id'))
    image = Column(String(255))
    superviseurs = relationship("Superviseurs", primaryjoin="Notifications.superviseur_id == Superviseurs.user_id")
    superviseurs = relationship("Superviseurs")
    # examuns = relationship("Examuns", primaryjoin="Notifications.id_exam == examuns.id")
    # examuns = relationship("Examuns")
class Superviseurs(Base):
    __tablename__ = 'superviseurs'

    user_id = Column(Integer, primary_key=True)

    
# class Examuns(Base):
#     __tablename__ = 'examuns'
#     id= Column(Integer, primary_key=True),
#     type=Column( String(250)),
#     heure_deb=Column(DateTime),
#     heure_fin=Column(DateTime),
#     id_mat=Column(Integer),
#     id_sal=Column(Integer),
    