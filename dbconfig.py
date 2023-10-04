from PIL import Image
from io import BytesIO
import deepface
from deepface import DeepFace
from pydantic import BaseModel
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column, Integer, String ,Sequence ,ForeignKey ,Date ,DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import relationship, mapper, sessionmaker
import os

from sqlalchemy import  Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from config.db import con
from models.departement import Departements
from models.filiere import Filieres
from models.matiere import Matiere
# from models.etudiermat import Etudiant
from models.etudiermat import Etudiant
from models.etudiermat import etudiermats
from models.etudiermat import Matiere
from models.semestre_etudiant import Semestres
from models.semestre_etudiant import semestre_etudiants
# from models.semestre_etudiant import Etudiants
from models.examun import examuns
from routes.historique import write_data_case_etudiant
from fastapi import APIRouter,Depends
from auth.authConfig import recupere_userid,create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from datetime import datetime, timedelta

Base = declarative_base()

# Create a session factory
Session = sessionmaker(bind=con)
# Create a session
session = Session()



Base.metadata.create_all(con)
def get_etudiant(photo: str):
    # print(photo)
    # Retrieve the student's ID after verifying the image
    etudiants = session.query(Etudiant.id).filter(Etudiant.photo == photo).all()
    id_etu = etudiants[0][0]
    return  id_etu
async def get_infoexamun(imagepath,image1: str,id_etu:int,user_id: int = Depends(recupere_userid),user: User = Depends(check_survpermissions)):
   
          #try:
             now = datetime.now()
    # print(now)
    # Check if the student has an exam at this moment
             subquery = session.query(etudiermats.c.id_mat).filter(etudiermats.c.id_etu == id_etu)
             exams = session.query(examuns.c.id).filter(and_(now >= examuns.c.heure_deb, now <= examuns.c.heure_fin, examuns.c.id_mat.in_(subquery))).all()
    # print("etudiant",id_etu)
             timestamp = datetime.now().timestamp()

             if not exams:
                       timestamp = datetime.now().timestamp()
                       notification_filename = f"{timestamp}.jpg"
                       notification_folder = "C:/Users/pc/StudioProjects/pfe/PFE_FRONT/images/notifications"
                       notification_path = os.path.join(notification_folder, notification_filename)
                       os.rename(imagepath, notification_path)

            # Nouveau chemin de l'image
                       image_etu_path = notification_path.replace("\\", "/")        
           
   
     
                       return await write_data_case_etudiant(image_etu_path,id_etu, user_id, user)
             else:   
                 return "Rentrez"
    
          #except Exception as e: