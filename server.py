from fastapi import FastAPI, File, UploadFile,HTTPException,Header,status,Depends,APIRouter
import uvicorn
#from prediction import read_image
from starlette.responses import JSONResponse
from prediction import predict_face
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, Column, Integer, String ,Sequence,and_
from sqlalchemy.ext.declarative import declarative_base
from fastapi.security import OAuth2PasswordRequestForm

import datetime
from auth.authConfig import recupere_userid,create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User

#auuth
#from fastapi import FastAPI, HTTPException, status
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker, relationship, Session

from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from auth.authConfig import get_current_user

# from routes.user import user_router
from routes.salle import salle_router
from routes.departement import departement_router
from routes.notification import notification_router
from routes.filiere import filiere_router
from routes.semestre import semestre_router
from routes.etudiant import etudiant_router
from routes.matiere import matiere_router
from routes.etudiermat import etudiermat_router
from routes.semestre_etudiant import semestre_etudiant_router
from routes.surveillance import surveillance_router
from routes.examun import examun_router
from routes.historique import historique_router
from fastapi.middleware.cors import CORSMiddleware
from config.db import con
from routes.historique import write_data,write_data_case_etudiant
app=FastAPI()
Session = sessionmaker(bind=con)
# Create a session
session = Session
#auth
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )
# Définir les routes pour l'ensemble d'itinéraires utilisateur
# app.include_router(user_router, prefix="", tags=["Utilisateurs"])

# Définir les routes pour l'ensemble d'itinéraires etudiant
app.include_router(etudiant_router, prefix="/etudiants", tags=["Etudiants"])

# Définir les routes pour l'ensemble d'itinéraires matiere
app.include_router(matiere_router, prefix="/matieres", tags=["Matieres"])

# Définir les routes pour l'ensemble d'itinéraires salle
app.include_router(semestre_etudiant_router, prefix="/semestre_etudiants", tags=["Semestre_etudiants"])

# Définir les routes pour l'ensemble d'itinéraires salle
app.include_router(salle_router, prefix="/salles", tags=["Salles"])

# Définir les routes pour l'ensemble d'itinéraires salle
app.include_router(etudiermat_router, prefix="/etudiermatiere", tags=["etudiermatiere"])

# Définir les routes pour l'ensemble d'itinéraires departement
app.include_router(departement_router, prefix="/departements", tags=["Departemens"])

# Définir les routes pour l'ensemble d'itinéraires notification
app.include_router(notification_router, prefix="/notifications", tags=["Notifications"])

# Définir les routes pour l'ensemble d'itinéraires filiere
app.include_router(filiere_router, prefix="/filieres", tags=["Filieres"])

# Définir les routes pour l'ensemble d'itinéraires semestre
app.include_router(semestre_router, prefix="/semestres", tags=["Semestres"])

# Définir les routes pour l'ensemble d'itinéraires examun
app.include_router(examun_router, prefix="/examuns", tags=["Examuns"])

# Définir les routes pour l'ensemble d'itinéraires surveillance
app.include_router(surveillance_router, prefix="/surveillances", tags=["Surveillances"])

# Définir les routes pour l'ensemble d'itinéraires historique
app.include_router(historique_router, prefix="/historiques", tags=["Historiques"])
# @app.get("/")
# async def home():
#     return {"message": "Bienvenue sur l'API de gestion des utilisateurs et des salles."}

@app.post("/registeruser/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email, "role": user.role},  # Inclusion du rôle dans les données du token
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/admin")
def admin_route(user: User = Depends(check_Adminpermissions)):
    return {"message": "Admin access granted"}

@app.get("/superv")
def superv_route(user: User = Depends(check_superviseurpermissions)):
    return {"message": "superviseur access granted"}

@app.get("/surveillant")
def surv_route(user: User = Depends(check_survpermissions)):
    return {"message": "superviseur access granted"}

#
@app.get('/')
def hello_world():
    return "hello world"


@app.post('/api/predict')
async def predict_image(file :UploadFile=File(...),user_id: int = Depends(recupere_userid),user: User = Depends(check_survpermissions)):
# async def predict_image(file :UploadFile=File(...)):
    #read file upload par user
    #image = read_image(file)
    #try:
        image = await file.read()
        with open("image.jpg", "wb") as f:
            f.write(image)
        result = await predict_face("image.jpg",user_id,user)
        #JSONResponse(content=result)
    #except Exception as e:
       # return {"error": str(e)}
        return result 



@app.get("/current_user")
def get_current_user_route(user: User= Depends(get_current_user)):

      user_data = {
        "id": user.id,
        "nom": user.nom,
        "prenom": user.prenom,
        "email": user.email,
        "role": user.role
                 }
      return user_data
@app.get("/test_his")
async def get_test(user_id: int = Depends(recupere_userid), user: User = Depends(check_survpermissions)):
    try:
        result = await write_data_case_etudiant(2, user_id, user)
        return result
    except Exception as e:
        # Gérer toutes les exceptions qui peuvent survenir pendant l'exécution
        print(f"Une erreur s'est produite : {str(e)}")
        return False

if __name__== "__main__":
   uvicorn.run(app,port=8000 ,host='127.0.0.1')
   #192.168.55.113
