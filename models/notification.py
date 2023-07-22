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
    superviseurs = relationship("Superviseurs", primaryjoin="Notifications.superviseur_id == Superviseurs.user_id")
    superviseurs = relationship("Superviseurs")
    
class Superviseurs(Base):
    __tablename__ = 'superviseurs'

    user_id = Column(Integer, primary_key=True)
    

    