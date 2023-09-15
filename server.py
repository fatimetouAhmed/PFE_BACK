from fastapi import FastAPI, File, UploadFile,HTTPException,Header,status,Depends,APIRouter,Form
import uvicorn
#from prediction import read_image
from starlette.responses import JSONResponse
from prediction import predict_face
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, Column, Integer, String ,Sequence,and_
from sqlalchemy.ext.declarative import declarative_base
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError,jwt
from passlib.context import CryptContext
import datetime
from auth.authConfig import user_router,recupere_userid,create_user,read_data_users,Superviseur,Surveillant,Administrateur,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
import redis
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
#auuth
#from fastapi import FastAPI, HTTPException, status
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker, relationship, Session

from auth.authConfig import create_user,UserResponse,UserCreate,read_users_nom,superviseur_id,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from auth.authConfig import get_current_user
import os
from models.etudiant import Etudiant
# from routes.user import user_router
from routes.salle import salle_router
from routes.departement import departement_router
from routes.notification import notification_router
from routes.filiere import filiere_router
from routes.semestre import semestre_router
from routes.etudiant import etudiant_router
from routes.semestresmatieres import semestresmatieres_router
from routes.departementssuperviseurs import departementssuperviseurs_router
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
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# origins = [
#     # Add the origins (domains) that you want to allow access from
#     "http://localhost:58144",
#     "http://your-another-origin.com",
#     # Add more origins if needed
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin (*)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Définir les routes pour l'ensemble d'itinéraires utilisateur
# app.include_router(user_router, prefix="", tags=["Utilisateurs"])

# Définir les routes pour l'ensemble d'itinéraires etudiant
app.include_router(etudiant_router, prefix="/etudiants", tags=["Etudiants"])
# Définir les routes pour l'ensemble d'itinéraires etudiant
app.include_router(user_router, prefix="/users", tags=["Users"])
# Définir les routes pour l'ensemble d'itinéraires departementssuperviseurs
app.include_router(departementssuperviseurs_router, prefix="/departementssuperviseurs", tags=["Departementssuperviseurs"])

# Définir les routes pour l'ensemble d'itinéraires semestresmatieres
app.include_router(semestresmatieres_router, prefix="/semestresmatieres", tags=["Semestresmatieres"])

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
async def create_user_route(nom: str= Form(...),
    prenom: str= Form(...),
    email: str= Form(...),
    pswd: str= Form(...),
    role: str= Form(...), id_surv: int= Form(...),file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    return await create_user(nom,prenom,email,pswd,role,db)
@app.put("/{id}")
async def update_data(id:int,usercreate:UserCreate,user: User = Depends(check_Adminpermissions)):
    con.execute(User.__table__.update().values(
        nom=usercreate.nom
    ).where(User.__table__.c.id==id))
    return await read_data_users()
@app.delete("/{id}")
async def delete_data(id:int,user: User = Depends(check_Adminpermissions)):
    con.execute(Superviseur.__table__.delete().where(Superviseur.__table__.c.user_id==id))
    con.execute(Surveillant.__table__.delete().where(Surveillant.__table__.c.user_id==id))
    con.execute(Administrateur.__table__.delete().where(Administrateur.__table__.c.user_id==id))
    con.execute(User.__table__.delete().where(User.__table__.c.id==id))
    return await read_data_users()
@app.get("/user_data/")
async def data_user_route():
    user_data = await read_data_users()
    return user_data
@app.get("/nomsuperviseur/")
async def data_user_nom():
    user_data = await read_users_nom()
    return user_data
@app.get("/id_superviseur/{nom}")
async def data_user_id(nom:str,user: User = Depends(check_Adminpermissions)):
    user_data = await superviseur_id(nom,user)
    return user_data
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

UPLOAD_FOLDER = Path("C:/Users/pc/StudioProjects/pfe/PFE_FRONT/images")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
@app.post("/upload/")
async def upload_image(file1: str):
    file: UploadFile = File(file1)
    try:
        # Obtenir l'extension du fichier
        file_extension = file.split(".")[-1]
        # Générer un nom de fichier unique
        file_name = f"{Path(file).stem}_{hash(file)}.{file_extension}"
        # Construire le chemin pour enregistrer le fichier
        file_path = UPLOAD_FOLDER / file_name

        with open(file1, "rb") as source_file:
            # Ouvrir le fichier de destination en mode écriture binaire
            with open(file_path, "wb") as dest_file:
                dest_file.write(source_file.read())
        
        return JSONResponse(content={"message": "Fichier téléversé avec succès"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Une erreur est survenue", "error": str(e)}, status_code=500)
@app.post('/api/predict')
async def predict_image(file: UploadFile = File(...), user_id: int = Depends(recupere_userid), user: User = Depends(check_survpermissions)):
    try:
        image = await file.read()
        with open("image.jpg", "wb") as f:
            f.write(image)
        result = await predict_face("image.jpg", user_id, user)
        return result
    except Exception as e:
        return {"error": str(e)}



@app.post('/api/pv')
async def pv(nom: str= Form(...),
    prenom: str= Form(...),
    genre: str= Form(...),
    date_N: datetime= Form(...),
    lieu_n: str= Form(...),
    email: str= Form(...),
    telephone: int = Form(...),
    nationalite: str = Form(...),
    date_insecription: datetime = Form(...),file: UploadFile = File(...), user_id: int = Depends(recupere_userid), db: Session = Depends(get_db)):
    try:
        image = await file.read()      
        # Spécifiez le chemin complet du dossier où vous souhaitez stocker l'image
        upload_folder = r"C:\Users\pc\StudioProjects\pfe\PFE_FRONT\images\etudiants"
       
        # Assurez-vous que le dossier existe, sinon, créez-le
        os.makedirs(upload_folder, exist_ok=True)      
        # Générez un nom de fichier unique (par exemple, basé sur le timestamp)
        unique_filename = f"{user_id}_{datetime.now().timestamp()}.jpg"   
        # Construisez le chemin complet du fichier
        file_path = os.path.join(upload_folder, unique_filename)  
        file_path_str = str(file_path).replace("\\", "/")
        print(file_path_str)
        # Enregistrez l'image dans le dossier spécifié
        with open(file_path, "wb") as f:
            f.write(image)
        print(file_path_str)    
        # date_N = datetime.strptime('2023-09-01T22:56:45.274Z', '%Y-%m-%dT%H:%M:%S.%fZ')
        # date_insecription = datetime.strptime('2023-09-01T22:56:45.274Z', '%Y-%m-%dT%H:%M:%S.%fZ')

        # Create a new Etudiant object
        etudiant = Etudiant(
            nom=nom,
            prenom=prenom,
            photo=str(file_path_str),
            genre=genre,
            date_N=date_N,
            lieu_n=lieu_n,
            email=email,
            telephone=telephone,
            nationalite=nationalite,
            date_insecription=date_insecription,
        )

        # Add the Etudiant object to the session and commit the changes
        db.add(etudiant)
        db.commit()

        return file_path_str
    except Exception as e:
        return {"error": str(e)}
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
@app.get("/current_user_id")
def get_current_user_route(user: User = Depends(get_current_user)):

    user_data = {
        "id": user.id,
        "nom": user.nom,
        "prenom": user.prenom,
        "email": user.email,
        "role": user.role
    }
    user_id = user_data["id"]
    return user_id
@app.get("/test_his")
async def get_test(user_id: int = Depends(recupere_userid), user: User = Depends(check_survpermissions)):
    try:
        result = await write_data_case_etudiant(2, user_id, user)
        return result
    except Exception as e:
        # Gérer toutes les exceptions qui peuvent survenir pendant l'exécution
        print(f"Une erreur s'est produite : {str(e)}")
        return False

#authentification
# ...

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ...

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

blacklisted_tokens = set()

    
@app.post("/logout/")
def logout(access_token: str = Depends(oauth2_scheme)):
    try:
        # Vérifier si le token a déjà été ajouté à la liste noire
        if access_token in blacklisted_tokens:
            raise HTTPException(status_code=401, detail="Token déjà révoqué")
        
        # Décoder le token d'accès pour obtenir son contenu (nom d'utilisateur et rôle)
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        role: str = payload.get("role")
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Token d'authentification invalide")

        # Ajouter le token à la liste noire
        blacklisted_tokens.add(access_token)

        return {"message": "Déconnexion réussie"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Token d'authentification invalide")

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host='127.0.0.1')
 
# 192.168.53.113  PUT /etudiants/32 HTTP/1.1" PUT /etudiant/2 HTTP/1.1"